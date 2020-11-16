from flask import Flask
from config import Configuration
#from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)