import os
import uuid
import requests
from supabase import create_client, Client
from Models.service_exception import *

class SupabaseService:
    def __init__(self):
        self.SUPABASE_URL = os.environ["SUPABASE_URL"]  
        self.SUPABASE_KEY = os.environ["SUPABASE_ANON_KEY"]  
        self.supabase: Client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def upload_to_supabase(self, image_url, bucket_name="images_generated"):
        try:

            fetch_response = requests.get(image_url)
            if fetch_response.status_code != 200:
                raise Exception(f"Error fetching image from URL: {fetch_response.text}")


            image_bytes = fetch_response.content  

            file_name = f"gen_{uuid.uuid4().hex}.png"

            self.supabase.storage.from_(bucket_name).upload(file_name, image_bytes, file_options={"content-type": "image/jpeg"})

            file_url = self.supabase.storage.from_(bucket_name).get_public_url(file_name)

            return file_url

        except requests.exceptions.RequestException as e:
            raise ServiceException(f"Request failed: {str(e)}", status_code=500)

        except ServiceException as e:
            raise ServiceException(f"Service error: {str(e)}", status_code=e.status_code)

        except Exception as e:
            raise ServiceException(f"Internal Server Error: {str(e)}", status_code=500)