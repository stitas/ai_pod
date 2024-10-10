from PIL import Image, ImageEnhance, ImageChops
import os
import json
import datetime

parent_dir = os.path.abspath('..')
product_data_json = open(os.path.join(parent_dir, 'products.json'))
product_data = json.load(product_data_json)

start = datetime.datetime.now()

def create_mockup(product_image_path, ai_image_path, filename, position, product_id):
    position = (position['x'], position['y'])
    product_image_size = (512, 512)
    ai_image_size = (200, 200)

    if(product_id == 4):
        ai_image_size = (150, 150)

    # print(product_image_path)

    product_image = Image.open(product_image_path).convert('RGBA')
    product_image = product_image.resize(product_image_size)

    ai_image = Image.open(ai_image_path).convert('RGBA')
    ai_image = ai_image.resize(ai_image_size)

    product_image.paste(ai_image, position)

    product_image.convert('RGBA').save(filename + '.png')

for product in product_data:
    for i in range(len(product['mockup_image_paths'])):
        filename = product['title'] + '_' + product['colors'][i] + '_mockup'
        mockup_path = os.path.join(parent_dir, 'mockup_images/' + product['mockup_image_paths'][i])
        position = product['position_mockup']
        product_id = product['id']
        create_mockup(mockup_path, r'C:\Users\Titas\Desktop\ai_pod\api\1024x1024.png', filename, position, product_id)

print(datetime.datetime.now() - start)
