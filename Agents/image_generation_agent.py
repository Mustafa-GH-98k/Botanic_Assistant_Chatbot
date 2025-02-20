import os
from openai import OpenAI
from pydantic import BaseModel
from Models.service_exception import ServiceException
from Services.supabase_service import SupabaseService

class ImageGenerationInput(BaseModel):
    prompt: str

def image_generation_agent(prompt: str) -> str:
    """Generate an image based on a prompt and upload it to Supabase.

    Args:
        prompt (str): The text-based prompt to generate the image.

    Returns:
        str: The URL of the stored image in Supabase.

    Raises:
        ServiceException: If there is an error during the image generation or upload process.

    Example:
        >>> agent = ImageGenerationAgent()
        >>> url = agent.image_generation_agent("A beautiful sunset over the mountains")
        >>> print(url)
        "https://supabase.example.com/storage/v1/object/public/images_generated/gen_abc123.png"
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    try:
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response.data[0].url

        supabase_service = SupabaseService()
        stored_img_url = supabase_service.upload_to_supabase(image_url)

        return stored_img_url

    except Exception as e:
        raise ServiceException(f"Failed to generate or upload image: {str(e)}")
