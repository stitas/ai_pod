from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    oauth_provider = db.Column(db.String(100), nullable=True) # Facebook or Google
    oauth_provider_id = db.Column(db.String, nullable=True)   
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, email, oauth_provider, oauth_provider_id):
        self.email = email
        self.oauth_provider = oauth_provider
        self.oauth_provider_id = oauth_provider_id

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    price = db.Column(db.Double)
    created = datetime.now()

    def __init__(self, user_id, price):
        self.user_id = user_id
        self.price = price

class Image(db.Model):
    __tablename__ = 'Image'
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(500))
    url = db.Column(db.String(500), nullable=True)

    def __init__(self, prompt, url):
        self.prompt = prompt
        self.url = url

    @property
    def serialize(self):
        return {
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

    @property
    def serialize(self):
        return {
            'title': self.title,
            'price': self.price,
            'color': self.color,
            'mockup_image_url': self.mockup_image_url,
            'ai_image_id': self.ai_image_id,
            'printful_product_id': self.printful_product_id
        }