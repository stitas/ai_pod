from PIL import Image
import os
import json
import io
import base64

parent_dir = os.path.abspath('..')
product_data_json = open(os.path.join(parent_dir, 'products.json'))
product_data = json.load(product_data_json)

# Returns bytes of image
def create_mockup(mockup_data):
    mockup_image_path = mockup_data['mockup_image_path']
    ai_image_path = mockup_data['ai_image_url']
    position = mockup_data['position']
    product_id = mockup_data['product_id']

    position = (position['x'], position['y'])
    mockup_image_size = (512, 512)
    ai_image_size = (200, 200)

    # If product is mug
    if(product_id == 4):
        ai_image_size = (150, 150)

    # Open and resize mockup image
    mockup_image = Image.open(mockup_image_path).convert('RGBA')
    mockup_image = mockup_image.resize(mockup_image_size)

    # Open and resize AI generated image
    ai_image = Image.open(ai_image_path).convert('RGBA')
    ai_image = ai_image.resize(ai_image_size)

    # Paste AI image on top of mockup
    mockup_image.paste(ai_image, position)

    # Byte array to store the image bytes
    img_byte_arr = io.BytesIO()

    # Saves img to byte array
    mockup_image.convert('RGBA').save(img_byte_arr, format='PNG')

    # Converts the byte array to base64 string
    img_base64_str = base64.b64encode(img_byte_arr.getvalue())

    return img_base64_str

# Function to get data of products ready for mockup generation
def get_mockup_data(ai_image_url):
    mockup_data = []

    for product in product_data:
        for i in range(len(product['mockup_image_paths'])):
            mockup_path = os.path.join(parent_dir, 'mockup_images/' + product['mockup_image_paths'][i])
            position = product['position_mockup']
            product_id = product['id']

            mockup_data.append({
                'mockup_image_path': mockup_path,
                'position': position,
                'product_id': product_id,
                'ai_image_url': ai_image_url
            })

    return mockup_data