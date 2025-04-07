from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
 
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

#Creates the application
app = Flask(__name__)
#Configures SQLite database, relative to the application instance folder
app.config.from_object(DevelopmentConfig)
#initialize the app with the extension
db.init_app(app)






