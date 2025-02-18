import os
import requests

from imgur.imgur_exceptions import ServiceException

class ImgurService:
    def __init__(self):
        self.CLIENT_ID = os.environ["IMGUR_CLIENT_ID"]

    def upload_to_imgur(self, image_url):
        url = "https://api.imgur.com/3/image"

        try:
            # Fetch image from the given URL
            fetch_response = requests.get(image_url, stream=True)
            if fetch_response.status_code != 200:
                raise ServiceException(f"Error fetching image from URL: {fetch_response.text}", status_code=fetch_response.status_code)

            # Set up headers with the Imgur Client-ID
            headers = {
                "Authorization": f"Client-ID {self.CLIENT_ID}"
            }

            # Upload the image to Imgur
            upload_response = requests.post(url, headers=headers, files={"image": fetch_response.raw})

            # Check the response status
            if upload_response.status_code != 200:
                raise ServiceException(f"Error uploading image: {upload_response.text}", status_code=upload_response.status_code)

            # Parse the response
            data = upload_response.json()
            if "data" not in data or "link" not in data["data"]:
                raise ServiceException("Error: Unexpected response structure from Imgur.", status_code=500)

            # Return the image URL
            return data["data"]["link"]

        except requests.exceptions.RequestException as e:
            raise ServiceException(f"Request failed: {str(e)}", status_code=500)

        except FileNotFoundError:
            raise ServiceException("Image file not found.", status_code=404)

        except Exception as e:
            raise ServiceException(f"Internal Server error: {str(e)}", status_code=500)