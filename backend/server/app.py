import hashlib
from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, jwt_required, get_jwt_identity
import pika
import pika.exceptions
from models import db, bcrypt, Image, Mockup, User
import json
import os
from dotenv import load_dotenv
import datetime
import requests
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

CORS(app, origins=[os.environ.get('FRONTEND_URL')])

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
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        response = jsonify({'login': 'success'})
        set_access_cookies(response, access_token) # Put jwt token in cookies (protection from xss)

        return response, 200

    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
# Return redirect to googles login screen url
# After login google redirects to react frontend with authorization code in params
@app.route('/login-google', methods=['GET'])
def login_google():
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    nonce = hashlib.sha256(os.urandom(1024)).hexdigest() # To protect from replay attack
    authorize_url = 'https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?'
    args = f'response_type=code&access_type=offline&client_id={str(os.environ.get('GOOGLE_CLIENT_ID'))}&redirect_uri={str(os.environ.get('FRONTEND_URL')) + '/authenticate-wait'}&scope=openid%20email%20profile&state={state}&nonce={nonce}'

    url = authorize_url + args

    return jsonify({'redirect_url':url}), 200

# Sets access token in cookies if google auth successful else 401 error code failed login
# Checks if google auth successful by authorization code
@app.route('/authorize-google', methods=['POST'])
def authorize_google():
    if request.method == 'POST':
        data = request.get_json(force=True)
        google_access_token_url='https://accounts.google.com/o/oauth2/token'
        google_userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
        
        authorization_data = {
            'code': data['authorization_code'],
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': os.environ.get('FRONTEND_URL') + '/authenticate-wait',
            'grant_type': 'authorization_code',
            'access_type': 'offline'
        }

        response = requests.post(google_access_token_url, json=authorization_data).json()

        if 'access_token' not in response:
            print(response)
            return jsonify({'error': 'Failed to exchange authorization code for access token'}), 401
        
        google_access_token = response['access_token']

        user_info = requests.post(google_userinfo_endpoint, headers={'Authorization': 'Bearer ' + google_access_token}).json()

        user = User.query.filter_by(oauth_provider='google', oauth_provider_id=user_info['sub']).first()

        if not user:
            user = User(user_info['email'], oauth_provider='google', oauth_provider_id=user_info['sub'])
            db.session.add(user)

        user.last_login = datetime.datetime.utcnow()
        db.session.commit()

        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=24))
        response = jsonify({'login': 'success'})
        set_access_cookies(response, access_token) # Put jwt token in cookies (protection from xss)

        return response, 200

    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
# Get all paginated imaages
@app.route('/get-images-paginate/', methods=['GET'])
def get_images_paginate():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get user generated images
    pagination = Image.query.paginate(page=page, per_page=per_page, error_out=False)

    images = [image.serialize() for image in pagination.items]

    if images:
        return jsonify({
            'images': images,
            'total': pagination.total,  # Total number of items in the database
            'page': pagination.page,  # Current page number
            'per_page': pagination.per_page,  # Number of items per page
            'pages': pagination.pages,  # Total number of pages
            'has_next': pagination.has_next,  # If there's a next page
            'has_prev': pagination.has_prev  # If there's a previous page   
        }), 200
    
    else:
        return jsonify({'error': 'No images found'}), 404
    
@app.route('/get-user-images-paginate/')
@jwt_required()
def get_user_images_paginate():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False) 

    images = [image.serialize() for image in pagination.items]

    if images:
        return jsonify({
            'images': images,
            'total': pagination.total,  # Total number of items in the database
            'page': pagination.page,  # Current page number
            'per_page': pagination.per_page,  # Number of items per page
            'pages': pagination.pages,  # Total number of pages
            'has_next': pagination.has_next,  # If there's a next page
            'has_prev': pagination.has_prev  # If there's a previous page   
        }), 200
    
    else:
        return jsonify({'error': 'No images found'}), 404

# Delete image from the database by id
@app.route('/delete-image/<image_id>', methods=['POST'])
@jwt_required()
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
@app.route('/create-mockup', methods=['POST'])
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
    
# Get mockups from database by id
@app.route('/get-mockups-by-ai-image-id/<ai_image_id>', methods=['GET'])
def get_mockups_by_ai_image_id(ai_image_id):
    mockups = Mockup.query.filter_by(ai_image_id=ai_image_id).all()
    data = []

    if mockups:
        for mockup in mockups:
            data.append(mockup.serialize()) 

        return jsonify(data), 200
    
    else:
        return jsonify({'error': 'Mockup with such ai image id was not found'}), 404

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
@app.route('/mockup-generator/create-task', methods=['POST'])
@jwt_required()
def create_mockup_task():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json(force=True)

        image = Image(data['prompt'], None, user_id)
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