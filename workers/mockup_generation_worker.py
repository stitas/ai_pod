import pika
import threading
from mockup_generation import mockup_generator, image_generation

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare('mockup_generation_queue', durable=True)

# TODO
# finish mockupgeneration task
# add multiprocessing

def callback(ch, method, properties, body):
    prompt = body.decode()

    image = image_generation.generate_image(prompt) # Returns image url
    mockup_data = mockup_generator.get_mockup_data(image)

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='mockup_generation_queue', on_message_callback=callback)
channel.start_consuming()