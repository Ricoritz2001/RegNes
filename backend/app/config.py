
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config shared across all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RAW_SHP_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'shapefiles')
    PROCESSED_GEOJSON = os.path.join(BASE_DIR, 'data', 'processed', 
                                     'regions_with_sentiment.geojson')


class ProductionConfig(Config):
    """Production-specific configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 
                                             'sqlite:///instance/flaskr.sqlite')


class DevelopmentConfig(Config):
    """Development environment config."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'flaskr.sqlite')}"

class TestingConfig(Config):
    """Testing-specific config."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/test_flaskr.sqlite'
