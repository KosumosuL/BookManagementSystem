from flask import jsonify, request, render_template, redirect, session, url_for
from BookManage.model import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
from datetime import datetime


def init_api(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        pass

    @app.route('/register', methods=['POST'])
    def register():
        pass


    @app.route('/manager_login', methods=['GET', 'POST'])
    def manager_login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config['MANAGER_NAME']:
                error = 'Invalid username'
            elif request.form['password'] != app.config['MANAGER_PWD']:
                error = 'Invalid password'
            else:
                session['user_id'] = app.config['MANAGER_NAME']
                return redirect(url_for('manager'))
        return render_template('manager_login.html', error=error)

    @app.route('/search', methods=['POST'])
    def search():
        pass