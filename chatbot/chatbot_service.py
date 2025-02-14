import base64
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

class ChatbotService :
    client : OpenAI

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    def generate_image(self, prompt: str, imageType:str):
        # Call OpenAI's DALL·E model to generate an image
        response = self.client.images.generate(prompt=prompt,
        n=1,  # Number of images to generate
        size="1024x1024"  
        )

        image_url = response.data[0].url
        image_response = requests.get(image_url)

        img_bytes = BytesIO(image_response.content)
        # img = Image.open(img_bytes)
        # img.show()

        if imageType == "base64":
            base64_str = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            return base64_str

        elif imageType == "image":
          return img_bytes
        # return send_file(img, mimetype='image/png') --> use in controller


    def chat(self, prompt:str):
        llm = ChatOpenAI()
        response = llm.invoke(prompt)
        return response.content

if __name__ == "__main__":
    chatbot = ChatbotService()
    r = chatbot.generate_image("beriut lebanon" , "base64")
    print(r)