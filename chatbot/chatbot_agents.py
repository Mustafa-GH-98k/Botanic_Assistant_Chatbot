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


from chatbot.chatbot_exceptions import ServiceException

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
        return image_url

    def image_analysis_agent(self , prompt:str , url : HttpUrl):
        client = OpenAI()
        url = str(url)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        image_description = response.choices[0].message.content
        return image_description

    def create_model_with_tools(self):
        llm = ChatOpenAI()


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
