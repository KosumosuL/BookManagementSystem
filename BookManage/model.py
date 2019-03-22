from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from flask_sqlalchemy import SQLAlchemy

from BookManage import db

class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.String(12), primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    phonenum = db.Column(db.String(11), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.ID

    def __init__(self, ID, name, password, phonenum):
        self.ID = ID
        self.name = name
        self.password = password
        self.phonenum = phonenum

    def get(self, ID):
        return self.query.filter_by(ID=ID).first()

    def add(self, user):
        db.session.add(user)
        return db.session_commit()

    # def update(self, user):
    #     db.session.update(user)
    #     return session_commit()

    def delete(self, ID):
        self.query.filter_by(ID=ID).delete()
        return db.session_commit()

    def out(self, user):
        return {
            'ID': user.ID,
            'name': user.name,
            'password': user.password,
            'phonenum': user.phonenum
        }

class Book(db.Model):
    __tablename__ = 'book'
    # limit ISBN format when input
    ISBN = db.Column(db.String(17), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    count = db.Column(db.INTEGER, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.ISBN

    def __init__(self, ISBN, name, category, address, count):
        self.ISBN = ISBN
        self.name = name
        self.category = category
        self.address = address
        self.count = count

    def get(self, ISBN):
        return self.query.filter_by(ISBN=ISBN).first()

    def add(self, book):
        db.session.add(book)
        return db.session_commit()

    # def update(self, user):
    #     db.session.update(user)
    #     return session_commit()

    def delete(self, ISBN):
        self.query.filter_by(ISBN=ISBN).delete()
        return db.session_commit()

    def out(self, book):
        return {
            'ISBN': book.ISBN,
            'name': book.name,
            'category': book.category,
            'address': book.address,
            'count': book.count
        }

class Switch(db.Model):
    __tablename__ = 'switch'
    SID = db.Column(db.INTEGER, primary_key=True, nullable=False)
    ISBN = db.Column(db.String(17), nullable=False)
    ID = db.Column(db.String(12), nullable=False)
    borrowtime = db.Column(db.Date, nullable=False)
    # SRETURNTIME = BORROWTIME + 2 month
    sreturntime = db.Column(db.Date, nullable=False)
    # if not none then returned
    returntime = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<Switch %r>' % self.SID

    def __init__(self, SID, ISBN, ID, borrowtime, sreturntime, returntime):
        self.SID = SID
        self.ISBN = ISBN
        self.ID = ID
        self.borrowtime = borrowtime
        self.sreturntime = sreturntime
        self.returntime = returntime

    def get(self, SID):
        return self.query.filter_by(SID=SID).first()

    def add(self, switch):
        db.session.add(switch)
        return db.session_commit()

    # def update(self, user):
    #     db.session.update(user)
    #     return session_commit()

    def delete(self, SID):
        self.query.filter_by(SID=SID).delete()
        return db.session_commit()

    def out(self, switch):
        return {
            'SID': switch.SID,
            'ISBN': switch.ISBN,
            'ID': switch.ID,
            'borrowtime': switch.borrowtime,
            'sreturntime': switch.sreturntime,
            'returntime': switch.returntime
        }