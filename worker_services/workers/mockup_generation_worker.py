import pika
import requests
import json
from dotenv import load_dotenv
import os
import time

from  mockup_generation import image_generation
from  mockup_generation import mockup_generator

load_dotenv()
SERVER_URL = os.environ.get('FLASK_SERVER_URL')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')


def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=5672))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ is not available, retrying in 5 seconds...")
            time.sleep(5)

def callback(ch, method, properties, body):
    data = json.loads(body) # Data passed from the rabbitmq message

    print('Received: ')
    print(data)

    image = image_generation.generate_image(data['prompt']) # Returns image url
    mockup_data = mockup_generator.get_mockup_data(image)

    for mockup in mockup_data:
        data_mockup = {
            'title': mockup['title'],
            'price': mockup['price'],
            'color': mockup['color'],
            'mockup_image_url': mockup['mockup_image_url'],
            'ai_image_id': data['ai_image_id'],
            'printful_product_id': mockup['printful_product_id']
        }

        requests.post(SERVER_URL + '/create-mockup', json=data_mockup)

    data_image = {
        'ai_image_url': image
    }

    requests.post(SERVER_URL + '/update-image/' + str(data['ai_image_id']), json=data_image)

    ch.basic_ack(delivery_tag = method.delivery_tag)

def start_consuming():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare('mockup_generation_queue', durable=True)
    print('waiting for messages')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='mockup_generation_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()