from flask import jsonify, request, render_template, redirect, session, url_for
from BookManage.model import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
from datetime import datetime


def init_api(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signin', methods=['POST'])
    def signin():
        try:
            ID = request.form.get('ID')
            password = request.form.get('pwd')
            ident = request.form.get('isadmin')
            print(ID)
            print(password)
            print(ident)
            if ident:
                if ID != app.config['MANAGER_ID']:
                    error = 'Invalid adminID'
                elif password != app.config['MANAGER_PWD']:
                    error = 'Wrong password'
                else:
                    session['ident'] = 'admin'
                    session['ID'] = ID
                    return redirect(url_for('admin'))
            else:
                user = User.get(User, ID)
                print(user)
                if user is None:
                    error = 'Invalid userID'
                elif password != user.password:
                    error = 'Wrong password'
                else:
                    session['ident'] = 'user'
                    session['ID'] = ID
                    return redirect(url_for('user'))
                print(error)
        except Exception as e:
            error = e
        return render_template('index.html', error=error)

    @app.route('/logout')
    def logout():
        session.clear()
        return render_template('index.html')

    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            ID = request.form.get('ID')
            name = request.form.get('name')
            password = request.form.get('pwd')
            phonenum = request.form.get('ph')

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

    @app.route('/admininfo', methods=['GET'])
    def admininfo():
        info = []
        books = Book.getall(Book)
        for book in books:
            book = Book.out(Book, book)
            # his = Switch.getbyISBN(Switch, ISBN=book['ISBN'])
            # histmp = []
            # for h in his:
            #     histmp.append(Switch.out(Switch, h))
            # info.append([book, histmp])
            info.append(book)
        print(info)
        limit = request.args.get('limit', 10)  # 每页显示的条数
        offset = request.args.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        return jsonify({'total': len(info), 'rows': info[int(offset):(int(offset) + int(limit))]})

    @app.route('/admin')
    def admin():
        check_admin()
        pinfo = [app.config['MANAGER_ID'], app.config['MANAGER_NAME'], app.config['MANAGER_PH']]
        return render_template('admin.html', pinfo=pinfo)


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
            # ISBN = request.form.get('ISBN')
            ISBN = request.args.get("ISBN")
            print(ISBN)
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

    @app.route('/userinfo', methods=['GET'])
    def userinfo():
        info = []
        his = Switch.getbyID(Switch, ID=session['ID'])
        for h in his:
            info.append(Switch.out(Switch, h))
        print(info)
        limit = request.args.get('limit', 10)  # 每页显示的条数
        offset = request.args.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)
        return jsonify({'total': len(info), 'rows': info[int(offset):(int(offset) + int(limit))]})

    @app.route('/user')
    def user():
        check_user()
        us = User.get(User, ID=session['ID'])
        us = User.out(User, us)
        pinfo = []
        for key, val in us.items():
            pinfo.append(val)
        print(pinfo)
        return render_template('user.html', pinfo=pinfo)

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

    @app.route('/resultinfo', methods=['GET'])
    def resultinfo():
        books = Book.getall(Book)
        target = request.args.get('target')
        print(target)
        result = []
        for book in books:
            book = Book.out(Book, book)
            print(book)
            ans = 0
            for i in range(len(target)):
                for j in range(i + 1, len(target) + 1):
                    ans += cal_relate(target[i:j], book['ISBN'] + ' ' + book['name'] + ' ' + book['author'] + ' ' + book['category'])
            if ans > 0:
                result.append([book, ans])
        result.sort(key=lambda relates: relates[1], reverse=True)
        info = []
        for book, ans in result:
            info.append(book)
        return jsonify(info)


    @app.route('/easysearch', methods=['POST'])
    def easysearch():
        target = request.form.get('target')
        return render_template('result.html', target=target)

    @app.route('/hsearch', methods=['POST'])
    def hsearch():
        pass