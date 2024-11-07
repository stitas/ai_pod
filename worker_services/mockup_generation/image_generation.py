import requests
from dotenv import load_dotenv
import os
import json
from .img_to_url import  upload_img_url

load_dotenv()

REPLICATE_TOKEN = os.environ.get('REPLICATE_TOKEN')

headers = {
    'Authorization': 'Bearer ' + REPLICATE_TOKEN,
    'Content-Type': 'application/json',
    'Prefer': 'wait',
}

# Generates image with AI and uploads to IMGBB and returns the url
def generate_image(prompt):
    json_data = {
        'input': {
            'prompt': prompt,
        },
    }

    response = requests.post(
        'https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions',
        headers=headers,
        json=json_data,
    )

    data = json.loads(response.text)

    while data['output'] is None:
        response = requests.get(data['urls']['get'], headers=headers)
        data = json.loads(response.text)

    ai_url = data['output'][0]

    url = upload_img_url(ai_url)

    return url

# Implement this if actually selling items to make the print quality better (MORE DPI)
# Upscales image from url and returns the upscalled image url
# def upscale_image(image_url):
#     json_data = {
#         'version': 'f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa',
#         'input': {
#             'image': image_url,
#             'scale': 3,
#         },
#     }

#     response = requests.post('https://api.replicate.com/v1/predictions', headers=headers, json=json_data)
#     data = json.loads(response.text)

#     while data['output'] is None:
#         response = requests.get(data['urls']['get'], headers=headers)
#         data = json.loads(response.text)

#     url = upload_img_url(data['output'])

#     return url