from PIL import Image
import os
import json
import io
import base64
from multiprocessing import Pool
from .img_to_url import upload_img_base64
import requests

# Load products.json
parent_dir = os.path.abspath('.')
product_data_json = open(os.path.join(parent_dir, 'products.json'))
product_data = json.load(product_data_json)

# Returns url of image
def create_mockup(mockup_image_path, ai_image_url, position, product_id):
    position = (position['x'], position['y'])
    mockup_image_size = (512, 512)
    ai_image_size = (200, 200)
    ai_image_bytes = requests.get(ai_image_url, stream=True).raw # Get image bytes from url

    # If product is mug
    if(product_id == 4):
        ai_image_size = (150, 150)

    # Open and resize mockup image
    mockup_image = Image.open(mockup_image_path).convert('RGBA')
    mockup_image = mockup_image.resize(mockup_image_size)

    # Open and resize AI generated image
    ai_image = Image.open(ai_image_bytes).convert('RGBA')
    ai_image = ai_image.resize(ai_image_size)

    # Paste AI image on top of mockup
    mockup_image.paste(ai_image, position)

    # Byte array to store the image bytes
    img_byte_arr = io.BytesIO()

    # Saves img to byte array
    mockup_image.convert('RGBA').save(img_byte_arr, format='PNG')

    # Converts the byte array to base64 string
    img_base64_str = base64.b64encode(img_byte_arr.getvalue())

    # Uploads image to the web and gets its url
    url = upload_img_base64(img_base64_str)

    return url

# Generates a tuple of args for one product to pass into create mockup
def generate_mockup_data(product, iteration, ai_image_url):
    mockup_path = os.path.join(parent_dir, 'mockup_images/' + product['mockup_image_paths'][iteration])
    position = product['position_mockup']
    product_id = product['id']

    return (mockup_path, ai_image_url, position, product_id)

# Function to get data of products ready for mockup generation
def get_mockup_data(ai_image_url):  
    gen_mock_data_args_list = []
    create_mock_args_list = []
    mockup_data = []
    urls = []

    # Get arg list and data about product
    for product in product_data:
        for i in range(product['item_count']):
            gen_mock_data_args_list.append((product, i, ai_image_url))
            mockup_data.append({
                'title': product['title_lt'],
                'price': product['price'],
                'color': product['colors_pretty'][i],
                'printful_product_id': product['printful_product_id']
            })

    # Generate mockups with multiprocessing
    with Pool() as pool:
        create_mock_args_list = pool.starmap(generate_mockup_data, gen_mock_data_args_list)
        urls = pool.starmap(create_mockup, create_mock_args_list)

    for i, mockup in enumerate(mockup_data):
        mockup['mockup_image_url'] = urls[i]

    return mockup_data