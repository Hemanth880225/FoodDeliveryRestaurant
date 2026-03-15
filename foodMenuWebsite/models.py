from sqlalchemy.orm import backref

from foodMenuWebsite import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False,default='default.webp')
    posts = db.relationship('Post', backref='author', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    is_owner = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}', '{self.email}')"

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Menu('{self.name}', '{self.category}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    def __repr__(self):
        return f"Order('{self.user_id}', '{self.date_ordered}')"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    menu_item = db.relationship('MenuItem', backref='order_items')

    def __repr__(self):
        return f"OrderItem('{self.order_id}', '{self.menu_item_id}', '{self.quantity}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text)

    def __repr__(self):
        return f"Message('{self.name}', '{self.email}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return f"Review('{self.user_id}', '{self.date}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    menu_item = db.relationship('MenuItem', backref='cart_items')

    def __repr__(self):
        return f"Cart('{self.user_id}', '{self.menu_item_id}', '{self.quantity}')"


