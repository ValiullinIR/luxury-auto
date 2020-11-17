from app import app, db
from flask import render_template, jsonify, redirect
from flask_restful import Resource, reqparse, request
from datetime import datetime
import base64

from models import Model, Car, Brand, Client, Order, orders_cars
import requests

@app.route('/')
def Index():
    return render_template('base.html')

@app.route('/admin', methods=['GET'])
def Admin():
    if request.method == 'POST':
        return 'hello'
    else:
        models = Model.query.all()
        brands = Brand.query.all()
        return render_template('Admin.html', brands=brands, models=models)

@app.route('/add_new_model', methods=['POST', 'GET'])
def Add_new_model():
    if request.method == 'POST':
        name = request.form['name']
        colors = request.form['possible_colors']
        data = request.form['release_year']
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        brand_id = int(request.form.get('brand_id'))
        brand = Brand.query.filter_by(id_brand=brand_id).first()
        model = Model(name=name, possible_color=colors, release_year=data, brand_id=brand.id_brand)
        try:
            db.session.add(model)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'DB adding error', 400


@app.route('/Add_new_brand', methods=['POST'])
def Add_new_brand():
    if request.method == 'POST':
        name = request.form['name']
        manufacturer_country = request.form['manufacturer-country']
        brand = Brand(name=name, manufacturer_country=manufacturer_country)

        try:
            db.session.add(brand)
            db.session.commit()
            return redirect('/admin')
        except:
            return "DB adding error", 400

@app.route('/Add_new_car', methods=['POST'])
def Add_new_car():
    if request.method == 'POST':
        color = request.form['color']
        power = int(request.form['power'])
        car_body = request.form['car_body']
        equipment = request.form['equipment']
        price = int(request.form['price'])
        photo = request.files['photo']
        photo_base64 = (base64.b64encode(photo.read())).decode()
        availability = False
        if request.form.get(availability):
            availability = True
        model_id = int(request.form.get('id_model'))
        car = Car(color=color, power=power, car_body=car_body, equipment=equipment, price=price, photo=photo_base64, order_id=1, model_id=model_id, availability=availability)
        try:
            db.session.add(car)
            db.session.commit()
            return render_template('img.html', img_base64=photo_base64)
        except:
            return 'Error'


@app.route('/add_new_client', methods=['POST'])
def Add_new_client():
    name=request.form['name']
    surname=request.form['surname']
    patronymic=request.form['patronymic']
    phone=request.form['phone']
    client = Client(name=name, surname=surname, patronymic=patronymic, phone=phone)
    db.session.add(client)
    db.session.commit()
    return 'Success'

@app.route('/db')
def DB():
    brands = Brand.query.all()
    models = Model.query.all()
    cars = Car.query.all()
    orders = Order.query.all()
    clients = Client.query.all()
    return render_template('db.html', brands=brands, models=models, cars=cars, orders=orders, clients=clients)