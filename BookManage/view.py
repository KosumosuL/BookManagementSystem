from flask import jsonify, request, render_template, redirect
from BookManage.model import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
from datetime import datetime

def init_api(app):

    @app.route('/')
    def index():
        return render_template('index.html')

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