from Pizza import db
from sqlalchemy.sql import func


class customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    password = db.Column(db.String, nullable=True)

    def __repr__(self):
        return self.name


class pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text)
    name = db.Column(db.String(25))
    price = db.Column(db.Integer)


class c_order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"))
    pizza_price = db.Column(db.Integer, db.ForeignKey("pizza.price"))
    pizza_name = db.Column(db.String)
