from PIL import Image
import os
import json

parent_dir = os.path.abspath('..')
product_data_json = open(os.path.join(parent_dir, 'products.json'))
product_data = json.load(product_data_json)

def create_mockup(product_image_path, ai_image_path, filename):
    position = (int((512-200) / 2), 150)
    ai_image_size = (200, 200)
    product_image_size = (512, 512)

    print(product_image_path)

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
        create_mockup(mockup_path, r'C:\Users\Titas\Desktop\ai_pod\api\img.jpg', filename)
