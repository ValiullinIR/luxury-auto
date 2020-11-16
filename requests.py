from app import app, db
from flask import redirect, url_for, render_template, jsonify
from flask_restful import request
from datetime import datetime
from werkzeug.utils import secure_filename
import base64

from models import Model, Brand, Car, Client, Order


@app.route('/models', methods=['POST', 'GET'])
def Add_model():
    if request.method == 'POST':
        json = request.get_json()
        name = json.get('name')
        colors = json.get('possible_colors')
        data = json.get('release_year')
        data += "-11-11T00:00"
        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        brand_id = int(json.get('brand_id'))
        brand = Brand.query.filter_by(id_brand=brand_id).first()
        model = Model(name=name, possible_color=colors, release_year=data, brand_id=brand.id_brand)

        db.session.add(model)
        db.session.commit()
        return 'Success!', 200
        return 'DB adding error', 400
    else:
        models = Model.query.all()
        return jsonify(models_list=[i.serialize for i in models])

@app.route('/models/<int:model_id>', methods=['PUT', 'DELETE'])
def Models(model_id):
    if request.method == 'PUT':
        model = Model.query.filter_by(id_model=model_id).first()
        json = request.get_json()
        name = json.get('name')
        if name != None:
            model.name = name
        colors = json.get('possible_colors')
        if colors != None:
            model.possible_color = colors
        data = json.get('release_year')
        if data != None:
            data += "-11-11T00:00"
            data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
            model.release_year = data
        brand_id = json.get('brand_id')
        if brand_id != None:
            model.brand_id = int(brand_id)
        try:
            db.session.commit()
            return 'Данные успешно обновлены!', 200
        except:
            return 'Ошибка обновления данных!', 500
    elif request.method == 'DELETE':
        Model.query.filter_by(id_model=model_id).delete()
        try:
            db.session.commit()
            return 'Запись успешно удалена',200
        except:
            return 'Ошибка удаления данных!', 500


@app.route('/brands', methods=['POST', 'GET'])
def Add_brand():
    if request.method == 'POST':
        json = request.get_json()
        name = json.get('name')
        manufacturer_country = json.get('manufacturer-country')
        brand = Brand(name=name, manufacturer_country=manufacturer_country)

        try:
            db.session.add(brand)
            db.session.commit()
            return 'Success', 200
        except:
            return "DB adding error", 400
    else:
        brands = Brand.query.all()
        #brands = jsonify(brands)
        return jsonify(brands_list = [i.serialize for i in brands])

@app.route('/brands/<int:brand_id>', methods=['PUT', 'DELETE'])
def Brands(brand_id):
    if request.method == 'PUT':
        brand = Brand.query.filter_by(id_brand=brand_id).first()
        json = request.get_json()
        name = json.get('name')
        if name != None:
            brand.name = name
        manufacturer_country = json.get('manufacturer-country')
        if manufacturer_country != None:
            brand.manufacturer_country = manufacturer_country

        try:
            db.session.commit()
            return 'Данные успешно обновлены!', 200
        except:
            return 'Ошибка обновления данных!', 500
    elif request.method == 'DELETE':
        Brand.query.filter_by(id_brand=brand_id).delete()
        try:
            db.session.commit()
            return 'Запись успешно удалена',200
        except:
            return 'Ошибка удаления данных!', 500


@app.route('/cars', methods=['POST','GET'])
def Cars():
    if request.method == 'POST':
        json = request.get_json()
        color = json.get('color')
        power = int(json.get('power'))
        car_body = json.get('car_body')
        equipment = json.get('equipment')
        photo = json.get('photo')
        price = int(json.get('price'))
        availability = bool(json.get('availability'))
        order_id = json.get('order_id')
        release_year = json.get('release_year')
        release_year += "-01-01T00:00"
        release_year = datetime.strptime(release_year, '%Y-%m-%dT%H:%M')
        if order_id != None:
            order_id = int(order_id)
        model_id = int(json.get('model_id'))
        model = Model.query.filter_by(id_model=model_id).first()
        brand = Brand.query.filter_by(id_brand=model.brand_id).first()
        name = brand.name + " " + model.name
        car = Car(name=name,color=color, price=price, power=power, car_body=car_body, equipment=equipment, photo=photo, order_id=order_id,
                  model_id=model_id, release_year=release_year, availability=availability)
        try:
            db.session.add(car)
            db.session.commit()
            return 'Success', 200
        except:
            return 'Error'
    else:
        cars = Car.query.all()
        return jsonify(cars_list=[i.serialize for i in cars])

@app.route('/cars/<int:id_car>', methods=['PUT','DELETE'])
def Cars_update(id_car):
    if request.method == 'PUT':
        car = Car.query.filter_by(id_car=id_car).first()
        json = request.get_json()
        color = json.get('color')
        if color != None:
            car.color = color
        power = json.get('power')
        if power != None:
            car.power = int(power)
        car_body = json.get('car_body')
        if car_body != None:
            car.car_body = car_body
        equipment = json.get('equipment')
        if equipment != None:
            car.equipment = equipment
        photo = json.get('photo')
        if photo != None:
            car.photo = photo
        price = json.get('price')
        if price != None:
            car.price = int(price)
        availability = bool(json.get('availability'))
        if availability != None:
            car.availability = availability
        order_id = json.get('order_id')
        if order_id != None:
            car.order_id = int(order_id)
        model_id = json.get('model_id')
        if model_id != None:
            model = Model.query.filter_by(id_model=model_id).first()
            brand = Brand.query.filter_by(id_brand=model.brand_id).first()
            name = brand.name + " " + model.name
            car.name = name
            car.model_id = int(model_id)
        release_year = str(json.get('release_year'))
        if release_year != None:
            release_year += "-01-01T00:00"
            release_year = datetime.strptime(release_year, '%Y-%m-%dT%H:%M')
            car.release_year = release_year
        try:
            db.session.commit()
            return 'Данные успешно обновлены!', 200
        except:
            return 'Ошибка обновления данных!', 500
    elif request.method == 'DELETE':
        Car.query.filter_by(id_car=id_car).delete()
        try:
            db.session.commit()
            return 'Запись успешно удалена', 200
        except:
            return 'Ошибка удаления данных!', 500

@app.route('/clients', methods=['POST', 'GET'])
def Clients():
    if request.method == "POST":
        json = request.get_json()
        name = json.get('name')
        surname = json.get('surname')
        patronymic = json.get('patronymic')
        phone = json.get('phone')
        client = Client(name=name, surname=surname, patronymic=patronymic, phone=phone)

        try:
            db.session.add(client)
            db.session.commit()
            return 'Success', 200
        except:
            return 'Client adding ERROR', 400
    else:
        clients = Client.query.all()
        return jsonify(client_list=[i.serialize for i in clients])

@app.route('/clients/<int:client_id>', methods=['PUT', 'DELETE'])
def Client_update(client_id):
    if request.method == "PUT":
        client=Client.query.filter_by(id=client_id).first()
        json = request.get_json()
        name = json.get('name')
        if name != None:
            client.name = name
        surname = json.get('surname')
        if surname != None:
            client.surname = surname
        patronymic = json.get('patronymic')
        if patronymic != None:
            client.patronymic = patronymic
        phone = json.get('phone')
        if phone != None:
            client.phone = phone
        try:
            db.session.commit()
            return 'Данные успешно обновлены!', 200
        except:
            return 'Ошибка обновления данных!', 500
    elif request.method == 'DELETE':
        Client.query.filter_by(id=client_id).delete()
        try:
            db.session.commit()
            return 'Запись успешно удалена', 200
        except:
            return 'Ошибка удаления данных!', 500


@app.route('/orders', methods=['POST', 'GET'])
def Orders():
    if request.method == 'POST':
        json = request.get_json()
        sum = int(json.get('sum'))
        data_time = datetime.strptime(json.get('data_time'), '%Y-%m-%dT%H:%M')
        client_id = json.get('client_id')

        order = Order(sum=sum, data_time=data_time, client_id=client_id)

        try:
            db.session.add(order)
            db.session.commit()
            return 'Success', 200
        except:
            return 'DB adding ERROR', 201
    else:
        orders = Order.query.all()
        return jsonify(orders_list=[i.serialize for i in orders])

@app.route('/orders/<int:order_id>', methods=['PUT', 'DELETE'])
def Order_update(order_id):
    if request.method == 'PUT':
        order = Order.query.filter_by(id_order=order_id).first()
        json = request.get_json()
        sum = json.get('sum')
        if sum != None:
            order.sum = int(sum)
        datetime = json.get('data_time')
        if datetime != None:
            data_time = datetime.strptime(json.get('data_time'), '%Y-%m-%dT%H:%M')
            order.data_time = data_time
        client_id = json.get('client_id')
        if client_id != None:
            order.client_id = int(client_id)
        try:
            db.session.commit()
            return 'Данные успешно обновлены!', 200
        except:
            return 'Ошибка обновления данных!', 500

    elif request.method == 'DELETE':
        Order.query.filter_by(id_order=order_id).delete()
        try:
            db.session.commit()
            return 'Запись успешно удалена', 200
        except:
            return 'Ошибка удаления данных!', 500

@app.route('/orders_of_one_client/<int:client_id>', methods=['GET'])
def Orders_of_one_client(client_id):
    if request.method == 'GET':
        orders = Order.query.filter_by(client_id=client_id)
        return jsonify(orders_list=[i.serialize for i in orders])

@app.route('/top_10_luxury_auto', methods=['GET'])
def Top_10_luxury_auto():
    if request.method == 'GET':
        cars = Car.query.order_by(Car.price.desc()).limit(10).all()
        return jsonify(cars_list=[i.serialize for i in cars])


@app.route('/cars_of_one_model/<int:model_id>', methods=['GET'])
def Cars_of_one_model(model_id):
    if request.method == 'GET':
        cars = Car.query.filter_by(model_id=model_id)
        return jsonify(cars_list=[i.serialize for i in cars])


@app.route('/models_of_one_year/<string:year>', methods=['GET'])
def Models_of_one_year(year):
    if request.method == 'GET':
        year += "-01-01T00:00"
        year = datetime.strptime(year, '%Y-%m-%dT%H:%M')
        models = Model.query.filter_by(release_year=year)
        return jsonify(models_list=[i.serialize for i in models])