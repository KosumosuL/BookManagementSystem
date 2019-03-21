from flask import jsonify, request
from BookManage.model import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
from datetime import datetime

def init_api(app):
    pass