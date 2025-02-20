import base64
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from pydantic import BaseModel , HttpUrl



class ImageAnalysisInput(BaseModel):
    """Input for image analysis."""
    prompt: str
    """The text-based prompt for the analysis."""
    url: HttpUrl
    """The URL of the image to analyze. Ensures URL is valid."""


def image_analysis_agent( prompt: str, url: HttpUrl):
    """
    Analyze an image by generating text based on a given prompt and image URL.

    Args:
        prompt (str): The text-based prompt for the analysis.
        url (HttpUrl): The URL of the image to analyze.

    Returns:
        str: The generated text that describes the image.

    Raises:
        requests.RequestException: If there is an error downloading the image.
        Exception: If there is an error opening the image.

    Example:
        >>> image_analysis_agent(self, "What's in this picture?", "https://example.com/image.jpg")
        "This is a picture of a cat."
    """
    client = OpenAI()
    url = str(url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise requests.RequestException(f"Error downloading image: {e}")

    try:
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        raise Exception(f"Error opening image: {e}")

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

