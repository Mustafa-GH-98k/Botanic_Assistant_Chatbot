import base64
import logging
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder

from chatbot.chatbot_agents import ChatbotAgentService


from .chatbot_exceptions import ServiceException

class ChatbotService :
    client : OpenAI
    image_options = ["base64" , "image"]

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    def generate_image(self, prompt: str, imageType: str):
        if imageType not in self.image_options:
            raise ServiceException(f"Image Type must be one of: {', '.join(self.image_options)}", 400)
        
        if not prompt.strip():
            raise ServiceException("Prompt cannot be empty.", 400)
        
        try:
            response = self.client.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
        except Exception as e:
            raise ServiceException(f"Failed to generate image: {str(e)}", 500)  

        try:
            image_url = response.data[0].url
            image_response = requests.get(image_url)

            if image_response.status_code != 200:
                raise ServiceException("Failed to fetch the generated image.", 502) 
            
            img_bytes = BytesIO(image_response.content)

        except requests.RequestException as e:
            raise ServiceException(f"Error fetching image: {str(e)}", 502)  
        
        if imageType == "base64":
            base64_str = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            return base64_str
        elif imageType == "image":
            return img_bytes


    def chat(self, prompt: str , user_session_id:str):
            if not prompt.strip():
                raise ServiceException("Prompt cannot be empty.", 400)

            try:
                client = firestore.Client(project=os.environ["FIREBASE_PROJECT_ID"])
                history = FirestoreChatMessageHistory(
                    session_id=user_session_id, collection=os.environ["FIREBASE_COLLECTION_NAME"], client=client
                )
                history.add_user_message(prompt)

                agent_service = ChatbotAgentService()
                llm = agent_service.create_model_with_tools()
                prompt_template= generate_prompt_template(history)

                chain = prompt_template | llm
                response = chain.invoke({"messages":history.messages})
                
                llm_response = response['messages'][-1].content

                history.add_ai_message(llm_response)

                return  llm_response
            except Exception as e:
                logging.exception("An unexpected error occurred")
                raise ServiceException(f"Internal Server Error", 500) 


def generate_prompt_template(history):
    context = """
    You are a chatbot that helps users by providing information and generating images based on their requests. 
    You can generate images and provide relevant information about them. 
    """

    # When the user requests an image, you should return as json the image url and text response .in this specific format  {{image_ur:"url" , response:"your text response here"}}
    # If the user asks about the image or follows up with a request related to the image, you should return the relevant image again, along with an appropriate explanation.

    task = """
    When a user asks a text based question, return a text-based answer. 
    When a user requests an image, generate the image,  return a json formatted response like so {{image_url : "url" , response : "text"}} that has the url to the image and your text response message to the user prompt input. 
    """
    # When a user asks about the image, refer to the previously generated image and provide an explanation or context.

    examplars = """
        Example 1:
        Input: What’s the capital of France?  

        Output: The capital of France is Paris.  

        Example 2:
        Input: Can you generate an image of a sunset?  

        Output:  
        {{  
            "image_url": "https://example.com/generated-sunset.jpg",  
            "response": "Here is the image of the sunset you requested."  
        }}  

        Example 3:
        Input: What is the image about?  

        Output: This image was generated to showcase a beautiful sunset, created based on your earlier request.  

        Example 4:
        Input: Can you show the sunset image again?  

        Output: Here is the sunset image you requested: [https://example.com/generated-sunset.jpg].  
"""


    instructions = """
    If the user asks for an image, return the image URL and a response strictly like this {{image_ur:"url" , response:"your text response here"}}. 
    If the user asks for more information about the image, provide details or context about the image. 
    Ensure consistency in response format for image generation."""

    # Combine all parts into a single prompt
    prompt = context + task + examplars
    # prompt = """
    # If a user asks for image generation you return your response as a json composed of {{"image_url":"url/to/image"}} , "response":"your text response to the user.
    # Strictly follow these rules with no fail, it's your mission
    # " 
    # """

    prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            prompt,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
    )

    return prompt_template



if __name__ == "__main__":
    chatbot = ChatbotService()
    r = chatbot.generate_image("beriut lebanon" , "base6")
    print(r)