import secrets
from flask import jsonify, request, send_file
import logging
from marshmallow import ValidationError
import base64
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langgraph.prebuilt import create_react_agent
from langchain.tools import StructuredTool
from pydantic import BaseModel , HttpUrl
from imgbb.imgbb_service import ImgbbService


from chatbot.chatbot_exceptions import ServiceException
from supabase_.supabase_service import SupabaseService

class ImageAnalysisInput(BaseModel):
    prompt: str
    url: HttpUrl  # Ensures URL is valid


class ImageGenerationInput(BaseModel):
    prompt: str

class ChatbotAgentService:
    def generate_image_agent(self , prompt: str):
        """Generate an image using OpenAI's DALL·E and return the image URL."""
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        response = client.images.generate(
                    prompt=prompt,
                    n=1,
                    size="1024x1024"
                )
        
        
        image_url = response.data[0].url

        supabase_service = SupabaseService()
        stored_img_url = supabase_service.upload_to_supabase(image_url)

        return stored_img_url

    def image_analysis_agent(self, prompt: str, url: HttpUrl):
        client = OpenAI()
        url = str(url)


        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Error downloading image: {e}"


        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            return f"Error opening image: {e}"


        image.thumbnail((512, 512))  # Adjust size as needed


        buffered = BytesIO()
        image.save(buffered, format="JPEG")  # Save in a compressed format
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")


        openai_response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        image_description = openai_response.choices[0].message.content
        return image_description

    def create_model_with_tools(self):
        llm = ChatOpenAI(model="gpt-4-turbo")


        image_tool = StructuredTool.from_function(
            func=self.generate_image_agent,
            name="image_generator",
            description="Generate an image from a given prompt using AI.",
            args_schema=ImageGenerationInput
        )

        image_analysis_tool = StructuredTool.from_function(
            func=self.image_analysis_agent,
            args_schema=ImageAnalysisInput,
            name="image_analyzer",
            description="Analyze an image by providing both a prompt and an image URL." 
        )

        agent = create_react_agent(
            model=llm, 
            tools=[image_tool, image_analysis_tool]
        )

        return agent
