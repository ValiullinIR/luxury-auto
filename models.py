from app import db
from datetime import datetime

orders_cars = db.Table('orders_cars',
                       db.Column('order_id', db.Integer, db.ForeignKey('order.id_order'), primary_key=True),
                       db.Column('car_id', db.Integer, db.ForeignKey('car.id_car'), primary_key=True)
                       )

# Модель - клиент
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(32))
    name = db.Column(db.String(32))
    patronymic = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    orders = db.relationship('Order', backref='client', lazy=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'name': self.name,
            'patronymic': self.patronymic,
            'phone': self.phone
        }


# Модель - заказ
class Order(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    data_time = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    cars = db.relationship('Car', secondary=orders_cars,  lazy='subquery',
                           backref=db.backref('cars', lazy=True))

    @property
    def serialize(self):
        cars_list = []
        for car in self.cars:
            cars_list = [i.serialize for i in self.cars]
            #cars_list.append(car.id_car)
        return {
            'id_order': self.id_order,
            'sum': self.sum,
            'data_time': datetime.__str__(self.data_time),
            'client_id': self.client_id,
            "cars_list": cars_list
        }


# Модель - марка
class Brand(db.Model):
    id_brand = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    manufacturer_country = db.Column(db.String(16))
    models = db.relationship('Model', backref='brand', lazy=True)

    @property
    def serialize(self):
        return {
            'id_brand': self.id_brand,
            'name': self.name,
            'manufacturer_country': self.manufacturer_country
        }


# Модель - модель
class Model(db.Model):
    id_model = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    possible_color = db.Column(db.Text)
    release_year = db.Column(db.DateTime)
    cars = db.relationship('Car', backref='model', lazy=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id_brand'), nullable=True)

    @property
    def serialize(self):
        brand = Brand.query.filter_by(id_brand=self.brand_id).first()
        return {
            'id_model': self.id_model,
            'name': self.name,
            'possible_color': self.possible_color,
            'release_year': datetime.__str__(self.release_year),
            'brand_id': self.brand_id,
            'brand_name': brand.name
        }


# Модель - авто
class Car(db.Model):
    id_car = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    color = db.Column(db.String(32))
    release_year = db.Column(db.DateTime, default=datetime.utcnow)
    power = db.Column(db.Integer)
    car_body = db.Column(db.String(32))
    price = db.Column(db.Integer)
    equipment = db.Column(db.String(32))
    photo = db.Column(db.Text)
    availability = db.Column(db.Boolean)
    orders = db.relationship('Order', secondary=orders_cars, lazy='subquery',
                             backref=db.backref('orders', lazy=True))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id_model'), nullable=False)

    @property
    def serialize(self):
        model = Model.query.filter_by(id_model=self.model_id).first()
        name = model.name
        return {
            'id_car': self.id_car,
            'name': self.name,
            'color': self.color,
            'release_year': datetime.__str__(self.release_year),
            'power': self.power,
            'car_body': self.car_body,
            'price': self.price,
            'equipment': self.equipment,
            'photo': self.photo,
            'availability': self.availability,
            'model_id': self.model_id,
            'model_name': name
        }

