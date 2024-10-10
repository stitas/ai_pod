from PIL import Image
import os
import json
import datetime
import io
import base64

parent_dir = os.path.abspath('..')
product_data_json = open(os.path.join(parent_dir, 'products.json'))
product_data = json.load(product_data_json)

start = datetime.datetime.now()

# Returns bytes of image
def create_mockup(product_image_path, ai_image_path, position, product_id):
    position = (position['x'], position['y'])
    product_image_size = (512, 512)
    ai_image_size = (200, 200)

    # If product is mug
    if(product_id == 4):
        ai_image_size = (150, 150)

    # Open and resize mockup image
    product_image = Image.open(product_image_path).convert('RGBA')
    product_image = product_image.resize(product_image_size)

    # Open and resize AI generated image
    ai_image = Image.open(ai_image_path).convert('RGBA')
    ai_image = ai_image.resize(ai_image_size)

    # Paste AI image on top of mockup
    product_image.paste(ai_image, position)

    # Byte array to store the image bytes
    img_byte_arr = io.BytesIO()

    # Saves img to byte array
    product_image.convert('RGBA').save(img_byte_arr, format='PNG')

    # Converts the byte array to base64 string
    img_base64_str = base64.b64encode(img_byte_arr.getvalue())

    return img_base64_str

def create_all_mockups():
    mockup_byte_data = []

    for product in product_data:
        for i in range(len(product['mockup_image_paths'])):
            mockup_path = os.path.join(parent_dir, 'mockup_images/' + product['mockup_image_paths'][i])
            position = product['position_mockup']
            product_id = product['id']

            mockup_byte_data.append(create_mockup(mockup_path, r'C:\Users\Titas\Desktop\ai_pod\api\1024x1024.png', position, product_id))

    return mockup_byte_data
