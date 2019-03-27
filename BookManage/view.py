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
            # print(ID)
            # print(password)
            # print(ident)
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
            info.append(book)
        # print(info)
        limit = request.args.get('limit', 10)  # 每页显示的条数
        offset = request.args.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        # print('get', limit)
        # print('get  offset', offset)
        return jsonify({'total': len(info), 'rows': info[int(offset):(int(offset) + int(limit))]})

    @app.route('/admin')
    def admin():
        check_admin()
        pinfo = {'ID':app.config['MANAGER_ID'], 'name':app.config['MANAGER_NAME'], 'phonenum':app.config['MANAGER_PH']}
        return render_template('admin.html', pinfo=pinfo, welcome='欢迎来到管理员空间')

    @app.route('/addbook', methods=['POST'])
    def addbook():
        check_admin()
        error = None
        welcome = None
        pinfo = {'ID': app.config['MANAGER_ID'], 'name': app.config['MANAGER_NAME'],
                 'phonenum': app.config['MANAGER_PH']}
        try:
            ISBN = request.form.get('ISBN')
            name = request.form.get('name')
            author = request.form.get('author')
            category = request.form.get('category')
            address = request.form.get('address')
            count = request.form.get('count')

            if Book.get(Book, ISBN):
                book = Book(
                    ISBN=ISBN,
                    name=name,
                    author=author,
                    category=category,
                    address=address,
                    count=Book.get(Book, ISBN=ISBN).count+count
                )
                _ = Book.update(Book, book)
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
            welcome = '书籍信息添加成功'
        except Exception as e:
            error = e
        return render_template('admin.html', pinfo=pinfo, error=error, welcome=welcome)

    @app.route('/delbook', methods=['POST'])
    def delbook():
        check_admin()
        error = None
        welcome = None
        pinfo = {'ID': app.config['MANAGER_ID'], 'name': app.config['MANAGER_NAME'],
                 'phonenum': app.config['MANAGER_PH']}
        try:
            # cannot be modified, thus donot check
            ISBN = request.form.get('ISBN')
            print(ISBN)
            _ = Book.delete(Book, ISBN=ISBN)
            welcome = '删除成功'
        except Exception as e:
            error = e
        return render_template('admin.html', pinfo=pinfo, error=error, welcome=welcome)

    @app.route('/modifybook', methods=['POST'])
    def modifybook():
        check_admin()
        error = None
        welcome = None
        pinfo = {'ID': app.config['MANAGER_ID'], 'name': app.config['MANAGER_NAME'],
                 'phonenum': app.config['MANAGER_PH']}
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
            welcome = '书籍信息修改成功'
        except Exception as e:
            error = e
        return render_template('admin.html', pinfo=pinfo, error=error, welcome=welcome)

    @app.route('/userinfo', methods=['GET'])
    def userinfo():
        info = []
        his = Switch.getbyID(Switch, ID=session['ID'])
        for h in his:
            info.append(Switch.out(Switch, h))
        # print(info)
        limit = request.args.get('limit', 10)  # 每页显示的条数
        offset = request.args.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        # print('get', limit)
        # print('get  offset', offset)
        return jsonify({'total': len(info), 'rows': info[int(offset):(int(offset) + int(limit))]})

    @app.route('/user')
    def user():
        check_user()
        us = User.get(User, ID=session['ID'])
        us = User.out(User, us)
        return render_template('user.html', pinfo=us, welcome='欢迎来到用户空间')

    @app.route('/modifyuser', methods=['POST'])
    def modifyuser():
        check_user()
        error = None
        welcome = None
        us = User.get(User, ID=session['ID'])
        us = User.out(User, us)
        try:
            # ID cannot be modified thus donot check ID's existence
            ID = request.form.get('ID')
            name = request.form.get('name')
            password = request.form.get('pwd')
            phonenum = request.form.get('ph')

            user = User(
                ID=session['ID'],
                name=name,
                password=password,
                phonenum=phonenum
            )
            _ = User.update(User, user)
            welcome = '个人信息修改成功'
        except Exception as e:
            error = e
        return render_template('user.html', pinfo=us, error=error, welcome=welcome)

    def cal_relate(tar, bookinfo):
        pos = bookinfo.find(tar)
        cnt = 0
        while pos != -1:
            cnt += 1
            pos = bookinfo.find(tar, pos+1)
        return cnt * len(tar) * len(tar) * len(tar)

    @app.route('/resultinfo', methods=['GET'])
    def resultinfo():
        target = request.args.get('target')
        target = target.replace('&#39;', '\'')
        target = eval(target)

        if target['mode'] == 'easy':
            books = Book.getall(Book)
            result = []
            target = target['tar']
            for book in books:
                book = Book.out(Book, book)
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
            # print(info)
            return jsonify(info)
        elif target['mode'] == 'strict':
            info = []
            if len(target['relat']) == 0:
                sql = 'SELECT * FROM book where ' + target['attr'][0] + '=\'' + target['sear'][0] + '\''
                books = Book.search(Book, sql)
                for book in books:
                    book = Book.out(Book, book)
                    info.append(book)
            else:
                sql = 'SELECT * FROM book where ' + target['attr'][0] + '=\'' + target['sear'][0] + '\''
                attr, sear, relat = target['attr'], target['sear'], target['relat']
                for i in range(len(relat)):
                    sql += ' ' + relat[i] + ' ' + attr[i+1] + '=\'' + sear[i+1] + '\''
                books = Book.search(Book, sql)
                for book in books:
                    book = Book.out(Book, book)
                    info.append(book)
            # print(info)
            return jsonify(info)
        else:
            pass

    @app.route('/easysearch', methods=['POST'])
    def easysearch():
        target = {}
        target['mode'] = 'easy'
        target['tar'] = request.form.get('target')
        return render_template('result.html', target=target)

    @app.route('/strictsearch', methods=['POST'])
    def strictsearch():
        target = {}
        try:
            row = request.form.get('row')
            row = int(row)
            attr, sear, relat = [], [], []
            attr_1 = request.form.get('attr_1')
            sear_1 = request.form.get('search_1')
            attr.append(attr_1)
            sear.append(sear_1)
            for i in range(2, row+1):
                relation = request.form.get('relation_' + str(i))
                attribute = request.form.get('attr_' + str(i))
                search = request.form.get('search_' + str(i))
                relat.append(relation)
                attr.append(attribute)
                sear.append(search)
            target['mode'] = 'strict'
            target['attr'] = attr
            target['sear'] = sear
            target['relat'] = relat
        except Exception as e:
            print(e)
        return render_template('result.html', target=target)

    @app.route('/search')
    def search():
        return render_template('search.html')