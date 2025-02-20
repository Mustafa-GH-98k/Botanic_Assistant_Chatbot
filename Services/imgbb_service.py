import os
import requests

from Models.service_exception import ServiceException

class ImgbbService:
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY") 

    def upload_to_imgbb(self , image_url):

        """
        Upload an image to imgbb.

        Args:
            image_url (str): The URL of the image.

        Returns:
            str: The URL of the uploaded image.

        Raises:
            ServiceException: If an exception occurs while fetching the image or uploading to imgbb.

        Example:
            imgbb_service = ImgbbService()
            image_url = imgbb_service.upload_to_imgbb("https://example.com/image.jpg")
            print(image_url)
        """
        
        url = "https://api.imgbb.com/1/upload"
        
        try:
            # with open(image_path, "rb") as image_file:
            #     upload_response = requests.post(url, data={"key": self.IMGBB_API_KEY}, files={"image": image_file})

            fetch_response = requests.get(image_url, stream=True)
            if fetch_response.status_code != 200:
                raise ServiceException(f"Error fetching image from URL: {fetch_response.text}", status_code=fetch_response.status_code)
            
            upload_response = requests.post(url, data={"key": self.IMGBB_API_KEY}, files={"image": fetch_response.raw})


            if upload_response.status_code != 200:
                raise ServiceException(f"Error uploading image: {upload_response.text}", status_code=upload_response.status_code)

            data = upload_response.json()
            if "data" not in data or "url" not in data["data"]:
                raise ServiceException("Error: Unexpected response structure from imgbb.", status_code=500)
            return data["data"]["url"]

        except requests.exceptions.RequestException as e:
            raise ServiceException(f"Request failed: {str(e)}", status_code=500)

        except FileNotFoundError:
            raise ServiceException("Image file not found.", status_code=404)

        except Exception as e:
            raise ServiceException(f"Internal Server error", status_code=500)

