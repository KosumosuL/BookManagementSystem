from datetime import timedelta

DEBUG = True
PORT = 5000
HOST = "localhost"

SECRET_KEY = "bookmanage"
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

MANAGER_ID = 'admin'
MANAGER_NAME = 'lucas'
MANAGER_PWD = '123456'
MANAGER_PH = '12345678901'