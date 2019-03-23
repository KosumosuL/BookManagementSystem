from datetime import timedelta

DEBUG = True
PORT = 5000
HOST = "localhost"

SECRET_KEY = "bookmanage"
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

MANAGER_NAME = 'admin'
MANAGER_PWD = '123456'