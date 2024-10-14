from flask import Flask, jsonify
import pika
import pika.exceptions

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

# TODO
# fill out these methods
# Pass mockup prompt to rabbitmq task

@app.route('/create-mockup')
def create_mockup():
    pass

@app.route('/get-mockup/<mockup_id>')
def get_mockup(mockup_id):
    pass

@app.route('/update-mockup/<mockup_id>')
def update_mockup(mockup_id):
    pass

@app.route('/delete-mockup/<mockup_id>')
def delete_mockup(mockup_id):
    pass

@app.route('/mockup-generator/create-task/<mockup_id>')
def create_mockup_task(mockup_id):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost:5672'))
    except pika.exceptions.AMQPConnectionError:
        return jsonify({'error': 'Failed to connect to RabbitMQ service. Message wont be sent.'})
    
    channel = connection.channel()
    channel.queue_declare('mockup_generation_queue', durable=True)

    channel.basic_publish(
        exchange = '',
        routing_key = 'mockup_generation_queue',
        properties = pika.BasicProperties(
            delivery_mode = pika.DeliveryMode.Persistent
        ),
    )

    connection.close()

    return 'Task started successfully'