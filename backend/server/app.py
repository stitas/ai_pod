import hashlib
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
import pika
import pika.exceptions
from models import db, bcrypt, Image, Mockup, User, CartItem, Order
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import requests
from flask_cors import CORS
import secrets

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

CORS(app, supports_credentials=True, origins=[os.environ.get('FRONTEND_URL')])

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
        
        user.last_login = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S:%f')
        db.session.commit()
        
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        csrf_token = secrets.token_hex(16)

        response = jsonify({'login': 'success'})

        response.set_cookie(
            'access_token_cookie',
            access_token,
            httponly=True,       
            secure=True,          
            samesite='None'        # Allows cross-origin requests
        )

        response.set_cookie(
            'csrf_access_token',
            csrf_token,
            httponly=True,       
            secure=True,          
            samesite='None'        # Allows cross-origin requests
        )

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

        user.last_login = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S:%f')
        db.session.commit()

        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
        response = jsonify({'login': 'success'})
        response.set_cookie(
            'access_token_cookie',
            access_token,
            httponly=True,       
            secure=True,          
            samesite='None'        # Allows cross-origin requests
        )

        return response, 200

    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    response.set_cookie(
            'access_token_cookie', 
            '',
            expires=0, 
            httponly=True,       
            secure=True,          
            samesite='None'
    )
    return response, 200

@app.route('/get-user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    if user:
        print(user.serialize())
        data = user.serialize()
        return jsonify(data), 200

    else:
        return jsonify({'error': 'User not found'}), 404

# Get image from the database by id
@app.route('/get-image/<image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.filter_by(id=image_id).first()

    if image:
        data = image.serialize()
        return jsonify(data), 200
    
    else:
        return jsonify({'error': 'Image with such id was not found'}), 404

# Get all paginated imaages
@app.route('/get-images-paginate', methods=['GET'])
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
    
@app.route('/get-user-images-paginate', methods=['GET'])
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
    
@app.route('/get-user-cart', methods=['GET'])
@jwt_required()
def get_user_cart():
    user_id = get_jwt_identity()
    
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    mockups = []

    # from each cart item gets the mockup and puts it in a mockup list which later returned
    if cart_items:
        for item in cart_items:
            mockup = Mockup.query.filter_by(id=item.mockup_id).first()
            mockup = mockup.serialize()
            mockup['quantity'] = item.quantity
            mockup['size'] = item.size
            mockups.append(mockup)

        return jsonify(mockups), 200
    else:
        return jsonify([]), 200
    
@app.route('/create-cart-item', methods=['POST'])
@jwt_required()
def create_cart_item():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json(force=True)
        
        cart_item = CartItem(user_id, data['mockup_id'], 1, data['size'])
        db.session.add(cart_item)
        db.session.commit()

        return 'Item created successfully', 201
        
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/update-cart-item', methods=['POST'])
@jwt_required()
def update_cart_item():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json(force=True)
        
        cart_item = CartItem.query.filter_by(user_id=user_id, mockup_id=data['mockup_id'], size=data['size']).first()
        cart_item.quantity = data['quantity']

        db.session.commit()

        return 'Cart item updated successfully', 200
        
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/delete-cart-item', methods=['POST'])
@jwt_required()
def delete_cart_item():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json(force=True)
        
        cart_item = CartItem.query.filter_by(user_id=user_id, mockup_id=data['mockup_id']).first()
        
        db.session.delete(cart_item)
        db.session.commit()

        return 'Cart item deleted successfully', 200
        
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/clear-cart', methods=['POST'])
@jwt_required()
def clear_cart():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return 'Cart cleared successfully', 200
        
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400
    
@app.route('/check-cart-item-exists/', methods=['POST'])
@jwt_required()
def check_cart_item_exists():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        data = request.get_json(force=True)
        
        cart_item = CartItem.query.filter_by(user_id=user_id, mockup_id=data['mockup_id'], size=data['size']).first()
        
        if cart_item:
            return jsonify({'quantity': cart_item.quantity}), 200
    
        return jsonify(False), 404
    
    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400

@app.route('/create-order', methods=['POST'])
def create_order():
    if request.method == 'POST':
        data = request.get_json(force=True)

        if data:
            order = Order(data['user_id'], data['order_price'])
            db.session.add(order)
            db.session.commit()

            body = {
                'order_id': order.id,
                'cart': data['cart']
            }

            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
            except pika.exceptions.AMQPConnectionError:
                return jsonify({'error': 'Failed to connect to RabbitMQ service. Message wont be sent.'}), 500
            
            channel = connection.channel()
            channel.queue_declare('product_printful_generation_queue', durable=True)

            channel.basic_publish(
                exchange = '',
                routing_key = 'product_printful_generation_queue',
                properties = pika.BasicProperties(
                    delivery_mode = pika.DeliveryMode.Persistent
                ),
                body=json.dumps(body)
            )

            connection.close()
            return jsonify({'order_id': order.id}), 200

    else:
        return jsonify({'error': 'Invalid request. Use POST request'}), 400

    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)