from dotenv import load_dotenv
from os import environ
import requests

load_dotenv()

PRINTFUL_TOKEN = environ.get('PRINTFUL_TOKEN')
HEADERS = {'Authorization': 'Bearer ' + PRINTFUL_TOKEN, 'Content-Type': 'application/json', 'Accept': 'application/json'}
URL_CREATE_PRODUCT = 'https://api.printful.com/store/products'
URL_GET_PRODUCT = 'https://api.printful.com/products'
URL_CREATE_ORDER = 'https://api.printful.com/orders'
URL_CREATE_SYNC_VAR = 'https://api.printful.com/store/products/{id}/variants'

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

    r = requests.post(URL_CREATE_PRODUCT, json=data, headers=HEADERS).json()

    return r['result']['id']

def get_printful_variant_id(product_id, size, color):

    r = requests.get(URL_GET_PRODUCT + '/' + str(product_id), headers=HEADERS).json()

    for variant in r['result']['variants']:
        # Tote bag no size
        if product_id == 367 and variant['color'] == color:
            return variant['id']
        
        # Mug
        if product_id == 19:
            variant['did']

        if variant['size'] == size and variant['color'] == color:
            return variant['id']
        
# Dummy info because no order form
def create_order(order_data):
    data = {
        'recipient': {
            'name': 'Monstras monstrelis',
            'address1': 'a',
            'address2': 'a',
            'city': 'Miestas',
            'country_code': 'LT',
            'country': 'Lithuania',
            'zip': '69420',
            'phone': '866666666',
            'email': 'monstras@gmail.com'
        },
        'items': order_data
    }


    print(data)
    r = requests.post(URL_CREATE_ORDER, json=data, headers=HEADERS)

    print(data)
    print(r.text)

    return r.text

def create_sync_variant(sync_product_id, variant_id, price, image_url):
    data = {
        'variant_id': variant_id,
        'retail_price': price,
        'files': [
            {
                'url':image_url
            }
        ]
    }

    r = requests.post(URL_CREATE_SYNC_VAR.format(id=sync_product_id), json=data, headers=HEADERS).json()

    print(r)

    return r['result']['id']
