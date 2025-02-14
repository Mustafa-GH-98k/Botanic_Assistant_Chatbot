import base64
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

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


    def chat(self, prompt: str):
            if not prompt.strip():
                raise ServiceException("Prompt cannot be empty.", 400)

            try:
                llm = ChatOpenAI()
                response = llm.invoke(prompt)
                return response.content
            except Exception as e:
                raise ServiceException(f"Failed to generate chat response: {str(e)}", 500) 

if __name__ == "__main__":
    chatbot = ChatbotService()
    r = chatbot.generate_image("beriut lebanon" , "base6")
    print(r)