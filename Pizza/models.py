from Pizza import db
from sqlalchemy.sql import func

class customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    active = db.Column(db.Boolean, nullable=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=True)
    def __repr__(self):
        return self.name

class pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    price = db.Column(db.Integer)
    
class c_order(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key = True)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"))

