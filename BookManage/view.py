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
        error = None
        try:
            ID = request.form.get('ID')
            password = request.form.get('password')
            ident = request.form.get('ident')

            if ident == 'admin':
                if ID != app.config['MANAGER_ID']:
                    error = 'Invalid adminID'
                elif password != app.config['MANAGER_PWD']:
                    error = 'Wrong password'
                else:
                    session['ident'] = 'admin'
                    session['ID'] = ID


                    return redirect(url_for('admin'))
            elif ident == 'user':
                user = User.get(User, ID)
                if user is None:
                    error = 'Invalid userID'
                elif password != user.password:
                    error = 'Wrong password'
                else:
                    session['ident'] = 'user'
                    session['ID'] = ID


                    return redirect(url_for('user'))
        except Exception as e:
            error = e
        return render_template('index.html', error=error)

    @app.route('/register', methods=['POST'])
    def register():
        error = None
        try:
            ID = request.form.get('ID')
            name = request.form.get('name')
            password = request.form.get('password')
            phonenum = request.form.get('phone')

            if User.get(User, ID):
                error = 'Existed userID'
            else:
                user = User(
                    ID=ID,
                    name=name,
                    password=password,
                    phonenum=phonenum
                )
                _ = User.add(User, user)
                session['ident'] = 'user'
                session['ID'] = ID
                return redirect(url_for('user'))
        except Exception as e:
            error = e
        return render_template('index.html', error=error)

    def check_admin():
        if session['ident'] != 'admin' or session['ID'] == '':
            error = 'Invalid admin, please login'
            return render_template('index.html', error=error)

    def check_user():
        if session['ident'] != 'user' or session['ID'] == '':
            error = 'Invalid user, please login'
            return render_template('index.html', error=error)

    @app.route('/admin', methods=['POST'])
    def admin():
        check_admin()
        info = []
        books = Book.getall(Book)
        for book in books:
            his = Switch.getbyISBN(Switch, ISBN=book.ISBN)
            info.append([book, his])
        return render_template('admin.html', info=info)

    @app.route('/delhis', methods=['POST'])
    def delhis():
        check_admin()
        error = None
        try:
            # cannot be modified, thus donot check
            SID = request.form.get('SID')

            _ = Switch.delete(Switch, SID=SID)
            return redirect(url_for('admin'))
        except Exception as e:
            error = e
        return render_template('admin.html', error=error)

    @app.route('/clearhis', methods=['POST'])
    def clearhis():
        check_admin()
        error = None
        try:
            # check his in the foreend to ensure ISBN existed in Switch
            ISBN = request.form.get('ISBN')

            _ = Switch.deletebyISBN(Switch, ISBN=ISBN)
            return redirect(url_for('admin'))
        except Exception as e:
            error = e
        return render_template('admin.html', error=error)

    @app.route('/addbook', methods=['POST'])
    def addbook():
        check_admin()
        error = None
        try:
            ISBN = request.form.get('ISBN')
            name = request.form.get('name')
            author = request.form.get('author')
            category = request.form.get('category')
            address = request.form.get('address')
            count = request.form.get('count')

            if Book.Book(Book, ISBN):
                book = Book(
                    ISBN=ISBN,
                    name=name,
                    author=author,
                    category=category,
                    address=address,
                    count=Book.get(Book, ISBN=ISBN).count+count
                )
                _ = Book.update(Book, book)
                return redirect(url_for('admin'))
            else:
                book = Book(
                    ISBN=ISBN,
                    name=name,
                    author=author,
                    category=category,
                    address=address,
                    count=count
                )
                _ = Book.add(Book, book)
                return redirect(url_for('admin'))
        except Exception as e:
            error = e
        return render_template('index.html', error=error)

    @app.route('/delbook', methods=['POST'])
    def delbook():
        check_admin()
        error = None
        try:
            # cannot be modified, thus donot check
            ISBN = request.form.get('ISBN')

            _ = Book.delete(Book, ISBN=ISBN)
            return redirect(url_for('admin'))
        except Exception as e:
            error = e
        return render_template('admin.html', error=error)

    @app.route('/modifybook', methods=['POST'])
    def modifybook():
        check_admin()
        error = None
        try:
            # ISBN cannot be modified thus donot check ID's existence
            ISBN = request.form.get('ISBN')
            name = request.form.get('name')
            author = request.form.get('author')
            category = request.form.get('category')
            address = request.form.get('address')
            count = request.form.get('count')

            book = Book(
                ISBN=ISBN,
                name=name,
                author=author,
                category=category,
                address=address,
                count=count
            )
            _ = Book.update(Book, book)
            return redirect(url_for('admin'))
        except Exception as e:
            error = e
        return render_template('index.html', error=error)

    @app.route('/user', methods=['POST'])
    def user():
        check_user()
        user = User.get(User, ID=session['ID'])
        his = Switch.getbyID(Switch, ID=user.ID)
        return render_template('user.html', info=[user, his])

    @app.route('/modifyuser', methods=['POST'])
    def modifyuser():
        check_user()
        error = None
        try:
            # ID cannot be modified thus donot check ID's existence
            ID = request.form.get('ID')
            name = request.form.get('name')
            password = request.form.get('password')
            phonenum = request.form.get('phone')

            user = User(
                ID=session['ID'],
                name=name,
                password=password,
                phonenum=phonenum
            )
            _ = User.update(User, user)
            return redirect(url_for('user'))
        except Exception as e:
            error = e
        return render_template('user.html', error=error)

    def cal_relate(tar, bookinfo):
        pos = bookinfo.find(tar)
        cnt = 0
        while pos != -1:
            cnt += 1
            pos = bookinfo.find(tar, pos+1)
        return cnt * len(tar) * len(tar) * len(tar)

    @app.route('/easysearch', methods=['POST'])
    def easysearch():
        books = Book.getall(Book)
        target = request.form.get('target')
        result = []
        for book in books:
            ans = 0
            for i in range(len(target)):
                for j in range(i + 1, len(target) + 1):
                    print(target[i:j])
                    ans += cal_relate(target[i:j], book.ISBN + ' ' + book.name + ' ' + book.author + ' ' + book.category)
            if ans > 0:
                result.append([book, ans])
        result.sort(key=lambda relates: relates[1], reverse=True)
        return render_template('result.html', result=result)

    @app.route('/hsearch', methods=['POST'])
    def hsearch():
        pass