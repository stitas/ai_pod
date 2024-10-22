from dotenv import load_dotenv
from os import environ
import requests

load_dotenv()

PRINTFUL_TOKEN = environ.get('PRINTFUL_TOKEN')
HEADERS = {'Authorization': 'Bearer ' + PRINTFUL_TOKEN, 'Content-Type': 'application/json', 'Accept': 'application/json'}
URL = 'https://api.printful.com/store/products'

# TODO
# find a way to pass variant id when user selects the size and color

# Created a new product in the printful shop 
def create_product(image_url, variant_id, order_id, price):
    data = {
        'sync_product': {
            'name': str(order_id),
            'thumbnail': image_url
        },
        'sync_variants': [
            {
            'variant_id': variant_id,
            'retail_price': str(price),
            'files': [
                {
                'type': 'default',
                'url': image_url,
                'visible': True
                }
            ],
            'availability_status': 'active'
            }
        ]
    }

    r = requests.post(URL, json=data, headers=HEADERS)

    return r.text