import base64
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from pydantic import BaseModel , HttpUrl



class ImageAnalysisInput(BaseModel):
    prompt: str
    url: HttpUrl  # Ensures URL is valid


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
            model="gpt-4o-mini",
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