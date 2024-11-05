from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

# TODO
# User modeli idet

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String, nullable=True)
    oauth_provider = db.Column(db.String(100), nullable=True) # Google
    oauth_provider_id = db.Column(db.String, nullable=True)   
    created = db.Column(db.String, default=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S:%f'))
    last_login = db.Column(db.String, default=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S:%f'))

    def __init__(self, email, oauth_provider, oauth_provider_id):
        self.email = email
        self.oauth_provider = oauth_provider
        self.oauth_provider_id = oauth_provider_id

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'oauth_provider': self.oauth_provider,
            'oauth_provider_id': self.oauth_provider_id,
            'created': self.created,
            'last_login': self.last_login
        }
    
class CartItem(db.Model):
    __tablename__ = 'CartItem'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    mockup_id = db.Column(db.Integer, db.ForeignKey('Mockup.id'))
    quantity = db.Column(db.Integer)
    size = db.Column(db.Integer, nullable=True)

    def __init__(self, user_id, mockup_id, quantity, size):
        self.user_id = user_id
        self.mockup_id = mockup_id
        self.quantity = quantity
        self.size = size
    

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)
    price = db.Column(db.Double)
    created = db.Column(db.String,  default=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S:%f'))

    def __init__(self, user_id, price):
        self.user_id = user_id
        self.price = price

class Image(db.Model):
    __tablename__ = 'Image'
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(500))
    url = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __init__(self, prompt, url, user_id):
        self.prompt = prompt
        self.url = url
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'url': self.url   
        }

class Mockup(db.Model):
    __tablename__ = 'Mockup'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Double)
    color = db.Column(db.String(100))
    mockup_image_url = db.Column(db.String(500))
    ai_image_id = db.Column(db.Integer, db.ForeignKey('Image.id'))
    printful_product_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))

    def __init__(self, title, price, color, mockup_image_url, ai_image_id, printful_product_id):
        self.title = title
        self.price = price
        self.color = color
        self.mockup_image_url = mockup_image_url
        self.ai_image_id = ai_image_id
        self.printful_product_id = printful_product_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'color': self.color,
            'mockup_image_url': self.mockup_image_url,
            'ai_image_id': self.ai_image_id,
            'printful_product_id': self.printful_product_id
        }