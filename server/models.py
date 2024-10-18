from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TODO
# User modeli idet

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