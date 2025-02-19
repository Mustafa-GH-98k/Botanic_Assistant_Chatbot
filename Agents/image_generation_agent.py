import os
from openai import OpenAI
from pydantic import BaseModel


from Services.supabase_service import SupabaseService

class ImageGenerationInput(BaseModel):
    prompt: str

def image_generation_agent(self , prompt: str):
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