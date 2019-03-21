
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
# from flask_sqlalchemy import SQLAlchemy

from BookManage import db

class User(db.Model):
    __tablename__ = 'user'
    stuID = db.Column(db.String(20), nullable=True)
    phonenum = db.Column(db.INTEGER, primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=True)
    major = db.Column(db.String(20), nullable=True)


    def __repr__(self):
        return '<User %r>' % self.phoneNum

    def __init__(self, phonenum, password, nickname, college, major, sex, stuID, srealname, jobID, trealname):
        self.phonenum = phonenum
        self.password = password
        self.nickname = nickname
        self.college = college
        self.major = major
        self.sex = sex
        self.stuID = stuID
        self.srealname = srealname
        self.jobID = jobID
        self.trealname = trealname

    def get(self, phonenum):
        return self.query.filter_by(phonenum=phonenum).first()

    def getall(self, classID):
        return self.query.filter(and_(JoinTable.classID == classID, JoinTable.stuID == User.stuID)).all()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    # def update(self, user):
    #     db.session.update(user)
    #     return session_commit()

    def delete(self, phonenum):
        self.query.filter_by(phonenum=phonenum).delete()
        return session_commit()

    def out(self, user):
        return {
            'phonenum': user.phonenum,
            'password': user.password,
            'nickname': user.nickname,
            'college': user.college,
            'major': user.major,
            'sex': user.sex,
            'stuID': user.stuID,
            'srealname': user.srealname,
            'jobID': user.jobID,
            'trealname': user.trealname
        }
