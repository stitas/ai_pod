from flask import Flask, jsonify, request
import pika
import pika.exceptions
from models import db, Image, Mockup

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

# TODO
# fill out these methods
# Pass image prompt to rabbitmq task
# create models

# Get image from the database by id
@app.route('/get-image/<image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.filter_by(id=image_id).first()

    if image:
        data = image.serialize()
        return 200, jsonify(data)
    
    else:
        return 404, jsonify({'error': 'Image with such id was not found'})

# Delete image from the database by id
@app.route('/delete-image/<image_id>', methods=['POST'])
def delete_image(image_id):
    if request.method == 'POST':
        image = Image.query.filter_by(id=image_id).first()

        db.session.delete(image)
        db.session.commit()

        return 200, 'Image deleted successfully'
    else:
        return 400, jsonify({'error': 'Invalid request. Use POST request'})

# Create a mockup
@app.route('/create-mockup/', methods=['POST'])
def create_mockup():
    if request.method == 'POST' and request.data:
        data = request.get_json(force=True)

        mockup = Mockup(data['title'], data['price'], data['color'], data['size'], data['mockup_image_url'], data['ai_image_url'], data['printful_product_id'], data['printful_variant_id'])
        db.session.add(mockup)
        db.session.commit()
    
        return 201, 'Mockup was successfully created'
    
    else:
        return 400, jsonify({'error': 'There was an error in creating the mockup'})

# Get mockup from database by id
@app.route('/get-mockup/<mockup_id>', methods=['GET'])
def get_mockup(mockup_id):
    mockup = Mockup.query.filter_by(id=mockup_id).first()

    if mockup:
        data = mockup.serialize()
        return 200, jsonify(data)
    
    else:
        return 404, jsonify({'error': 'Mockup with such id was not found'})

# Delete mockup from database by id
@app.route('/delete-mockup/<mockup_id>', methods=['POST'])
def delete_mockup(mockup_id):
    if request.method == 'POST' and request.data:
        mockup = mockup.query.filter_by(id=mockup_id).first()

        db.session.delete(mockup)
        db.session.commit()

        return 'Mockup deleted successfully'
    else:
        return 400, jsonify({'error': 'Invalid request. Use POST request'})

# Creates a mockup generation task with RabbitMQ and returns the image id to which mockups will be generated
@app.route('/image-generator/create-task/', methods=['POST'])
def create_mockup_task():
    if request.method == 'POST':
        data = request.get_json(force=True)
        prompt = data['prompt']

        image = Image(prompt, None)

        db.session.add(image)
        db.session.commit()

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost:5672'))
        except pika.exceptions.AMQPConnectionError:
            return 500, jsonify({'error': 'Failed to connect to RabbitMQ service. Message wont be sent.'})
        
        channel = connection.channel()
        channel.queue_declare('image_generation_queue', durable=True)

        channel.basic_publish(
            exchange = '',
            routing_key = 'image_generation_queue',
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            ),
            body=prompt
        )

        connection.close()

        return 200, jsonify({'image_id': image.id})
    
    else:
        return 400, jsonify({'error': 'Invalid request. Use POST request'})