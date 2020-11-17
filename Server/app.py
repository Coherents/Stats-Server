from flask import *
from flask_login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from forms import *
from flask_migrate import Migrate
from flask_sqlalchemy import *
import os
import sqlite3
import pymongo
import sys
from werkzeug.security import  generate_password_hash, check_password_hash
from datetime import datetime
PATH=os.getcwd()

with open('req.txt','r') as file:
    auth=file.read()

app=Flask(__name__)
app.config["SECRET_KEY"]='asdasd'
app.config["SQLALCHEMY_DATABASE_URI"]=auth
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db = SQLAlchemy(app)
login=LoginManager(app)
class Account(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(1000),unique=False,nullable=False)
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
    def __repr__(self):
        return self.username


@login.user_loader
def validate(user):
	return Account.query.get(int(user))

@app.route('/')
@app.route('/<name>')
@login_required
def index(name=None,mo:bool=False):
    if name!=None:
        
        return render_template('index.html',name=name)
    else:
        return render_template('index.html')
@app.route("/register",methods=["GET","POST"])
def register():
	form=Register()
	if form.validate_on_submit():
		users=Account(username=form.username.data,email=form.email.data,password=generate_password_hash(form.password.data))
		session["file"]=form.file.data.filename
		try:
			print(session["file"])
		except:
			pass
		db.session.add(users)
		db.session.commit()
		return redirect (url_for("login"))
	return render_template("register.html",form=form)
@app.route("/login",methods=["GET","POST"])
def login():
	form=Login()
	n=None
	if form.validate_on_submit():
		D=Account.query.filter_by(email=form.email.data).first()
		
		if D:
			n=D.username
			if not check_password_hash(D.password,form.password.data):
				data=False
				session["EMAIL"]=form.email.data
				
				return redirect(url_for("change_password",user=session["EMAIL"]))
			
				
		else:
			return redirect(url_for("register"))
			
		
		login_user(D,remember=form.remember_me.data)
		
		return redirect(url_for("index",name=n))
		
	return render_template("login.html",form=form)

@app.errorhandler(401)
def error1(error):
    return "<h1><center> Not Authorized</center></h1>"

if __name__=='__main__':
   app.run(debug=True)