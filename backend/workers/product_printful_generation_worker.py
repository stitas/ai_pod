import pika
import json

from mockup_generation import product_printful_generator

def callback(ch, method, properties, body):
    data = json.loads(body) # Data passed from the rabbitmq message

    order_data = []
    print('Received: ')
    print(data)

    for i, item in enumerate(data['cart']):
        variant_id = product_printful_generator.get_printful_variant_id(item['printful_product_id'], item['size'], item['color'])
        sync_product_id = product_printful_generator.create_product(item['mockup_image_url'], variant_id, str(data['order_id']) + '_' + str(i), item['price'])
        sync_variant_id = product_printful_generator.create_sync_variant(sync_product_id, variant_id, item['price'], item['mockup_image_url'])

        item = {
            'quantity': item['quantity'],
            'retail_price': item['price'],
            'name': item['title'],
            'sync_variant_id': sync_variant_id,
            'source': 'sync'
        }

        order_data.append(item)

    product_printful_generator.create_order(order_data)

    ch.basic_ack(delivery_tag = method.delivery_tag)

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare('product_printful_generation_queue', durable=True)
    print('waiting for messages')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='product_printful_generation_queue', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()