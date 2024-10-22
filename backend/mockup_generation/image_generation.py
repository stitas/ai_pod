import requests
from dotenv import load_dotenv
import os
import json
from .img_to_url import upload_img_base64, upload_img_url

load_dotenv()

REPLICATE_TOKEN = os.environ.get('REPLICATE_TOKEN')

headers = {
    'Authorization': 'Bearer ' + REPLICATE_TOKEN,
    'Content-Type': 'application/json',
    'Prefer': 'wait',
}

# {
#   "id": "n05kh1h3v5rm40cjhg3tve4pbw",
#   "model": "black-forest-labs/flux-schnell",
#   "version": "dp-4d0bcc010b3049749a251855f12800be",
#   "input": {
#     "prompt": "Jesus dunking on the devil in an NBA finals game while wearing the chicago bulls jersey with the number 1"
#   },
#   "logs": "",
#   "output": [base64 string],
#   "data_removed": false,
#   "error": null,
#   "status": "processing",
#   "created_at": "2024-10-14T17:15:31.161Z",
#   "urls": {
#     "cancel": "https://api.replicate.com/v1/predictions/n05kh1h3v5rm40cjhg3tve4pbw/cancel",
#     "get": "https://api.replicate.com/v1/predictions/n05kh1h3v5rm40cjhg3tve4pbw",
#     "stream": "https://stream.replicate.com/v1/files/wcdb-shtqxq7mvjpctbedb2oarsx73udqojvovfvbj4bplh75bog76yea"
#   }
# }

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

    base64_string = data['output'][0]
    base64_string = base64_string.split(',', 1)[1] # Cut everything up to the first comma where the base64 string of image starts

    url = upload_img_base64(base64_string)

    return url

# Upscales image from url and returns the upscalled image url
def upscale_image(image_url):
    json_data = {
        'version': 'f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa',
        'input': {
            'image': image_url,
            'scale': 3,
        },
    }

    response = requests.post('https://api.replicate.com/v1/predictions', headers=headers, json=json_data)
    data = json.loads(response.text)

    while data['output'] is None:
        response = requests.get(data['urls']['get'], headers=headers)
        data = json.loads(response.text)

    url = upload_img_url(data['output'])

    return url

# print(generate_image('A blue peugeot 206 gone of the road and face first in the ditch. The road is snowy and there are tire marks of the car going of the road. The number plates of the peuegot are HCL 206'))
# print(upscale_image('https://i.ibb.co/CVMHQZQ/download.webp'))