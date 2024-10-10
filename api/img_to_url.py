import requests
from dotenv import load_dotenv
from os import environ
import base64

load_dotenv()

IMGBB_TOKEN = environ.get('IMGBB_TOKEN')
URL = 'https://api.imgbb.com/1/upload'

IMGBB_PARAMS = {
    'key': IMGBB_TOKEN
}

def upload_img(img_url):
    img_base64 = base64.b64encode(requests.get(img_url)).content

    files = {
        'image': (None, img_base64)
    }

    response = requests.post(URL, params=IMGBB_PARAMS, files=files).text
    img_url = response['data']['url']

    return response.text