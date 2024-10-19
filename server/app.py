from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
import pika
import pika.exceptions
from models import db, bcrypt, Image, Mockup, User
import json
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = User.query.filter_by(email=data['email']).first()

        if user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        user = User(data['email'], None, None)
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify('User created successfully'), 201
            
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        user = User.query.filter_by(email=data['email']).first()

        # If user email or password is incorrect return
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'})
        
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))

        return jsonify({'access_token': access_token}), 200

    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400

# Get image from the database by id
@app.route('/get-image/<image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.filter_by(id=image_id).first()

    if image:
        data = image.serialize()
        return jsonify(data), 200
    
    else:
        return jsonify({'error': 'Image with such id was not found'}), 404

# Delete image from the database by id
@app.route('/delete-image/<image_id>', methods=['POST'])
def delete_image(image_id):
    if request.method == 'POST':
        image = Image.query.filter_by(id=image_id).first()

        if image:
            db.session.delete(image)
            db.session.commit()

            return 'Image deleted successfully', 200
        
        else:
            return jsonify({'error': 'Image with such id was not found'}), 404
    
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400

@app.route('/update-image/<image_id>', methods=['POST'])
def update_image(image_id):
    if request.method == 'POST':
        data = request.get_json(force=True)
        image = Image.query.filter_by(id=image_id).first()

        if image:
            image.url = data['ai_image_url']
            db.session.commit()

            return 'Image updated successfully', 200
        
        else:
            return jsonify({'error': 'Image with such id was not found'}), 404
    
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400

# Create a mockup
@app.route('/create-mockup/', methods=['POST'])
def create_mockup():
    if request.method == 'POST' and request.data:
        data = request.get_json(force=True)

        mockup = Mockup(data['title'], data['price'], data['color'], data['mockup_image_url'], data['ai_image_id'], data['printful_product_id'])
        db.session.add(mockup)
        db.session.commit()
    
        return 'Mockup was successfully created', 201
    
    else:
        return jsonify({'error': 'There was an error in creating the mockup'}), 400

# Get mockup from database by id
@app.route('/get-mockup/<mockup_id>', methods=['GET'])
def get_mockup(mockup_id):
    mockup = Mockup.query.filter_by(id=mockup_id).first()

    if mockup:
        data = mockup.serialize()
        return jsonify(data), 200
    
    else:
        return jsonify({'error': 'Mockup with such id was not found'}), 404

# Delete mockup from database by id
@app.route('/delete-mockup/<mockup_id>', methods=['POST'])
def delete_mockup(mockup_id):
    if request.method == 'POST' and request.data:
        mockup = mockup.query.filter_by(id=mockup_id).first()

        db.session.delete(mockup)
        db.session.commit()

        return 'Mockup deleted successfully', 200
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 404

# Creates a mockup generation task with RabbitMQ and returns the image id to which mockups will be generated
@app.route('/mockup-generator/create-task/', methods=['POST'])
def create_mockup_task():
    if request.method == 'POST':
        data = request.get_json(force=True)

        image = Image(data['prompt'], None)
        db.session.add(image)
        db.session.commit()

        body = {
            'prompt': data['prompt'],
            'ai_image_id': image.id
        }

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        except pika.exceptions.AMQPConnectionError:
            return jsonify({'error': 'Failed to connect to RabbitMQ service. Message wont be sent.'}), 500
        
        channel = connection.channel()
        channel.queue_declare('mockup_generation_queue', durable=True)

        channel.basic_publish(
            exchange = '',
            routing_key = 'mockup_generation_queue',
            properties = pika.BasicProperties(
                delivery_mode = pika.DeliveryMode.Persistent
            ),
            body=json.dumps(body)
        )

        connection.close()

        return jsonify({'image_id': image.id}), 200
    
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)