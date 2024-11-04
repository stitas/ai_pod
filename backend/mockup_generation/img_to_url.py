import requests
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

IMGBB_TOKEN = os.environ.get('IMGBB_TOKEN')
URL = 'https://api.imgbb.com/1/upload'

IMGBB_PARAMS = {
    'key': IMGBB_TOKEN
}

def upload_img_url(img_url):
    img_base64 = base64.b64encode(requests.get(img_url).content)

    files = {
        'image': (None, img_base64)
    }

    response = requests.post(URL, params=IMGBB_PARAMS, files=files)
    response = json.loads(response.text)
    img_url = response['data']['url']

    return img_url

def upload_img_base64(img_base64):
    files = {
        'image': (None, img_base64)
    }

    response = requests.post(URL, params=IMGBB_PARAMS, files=files)
    response = json.loads(response.text)

    img_url = response['data']['url']

    return img_url