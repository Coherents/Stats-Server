from flask import *
from flask_login import LoginManager,current_user,login_required,login_user,logout_user,UserMixin
from collections import defaultdict
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
sess={}
sess['name']=None
with open('req.txt','r') as file:
    auth=file.read()
L={}
app=Flask(__name__)
app.config["SECRET_KEY"]='asdasd'
app.config["SQLALCHEMY_DATABASE_URI"]=auth  # psql used 
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

@app.route('/<name>')
@app.route('/')
@login_required
def index(name=None):
    
    if name!=None:
            return render_template('index.html',name=name) 
    else:
            return render_template('index.html',name=sess['name'])
   
        

  
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
    if  current_user.is_authenticated:
        return redirect(url_for('index'))
    form=Login()
    if form.validate_on_submit():
            D=Account.query.filter_by(email=form.email.data).first()
            n=D.username
            if D:
                    if not check_password_hash(D.password,form.password.data):
                            data=False
                            sess["Email"]=form.email.data
                            return redirect('index',user=sess['Email'])
            else:
                    return redirect(url_for('register'))
            login_user(D,remember=form.remember_me.data)
            sess['name']=n
            return redirect(url_for('index',name=sess['name']))
    return render_template('login.html',form=form)
    #return render_template('login.html',form=form)

                    
@app.route('/read')
def commercial():
    return render_template('readData.html',List=L.keys(),D=L)
@app.route('/hola',methods=["GET",'POST'])
def post_route():
     data=request.form["category_text"]
     if data not in L.keys():
            L[data]=[]
    
     print(L)
     print(data)
     return render_template('readData.html',List=L.keys(),D=L)


@app.route('/yolo/<name>')
def yolo(name=None):
        if name:
                return render_template('yolo.html',name=name)
        else:
                return redirect(url_for('index'))

@app.route('/qwert/<name>',methods=["GET","POST"])
def fuck(name=None):
        if name:
                Item=request.form["item"]
                L[name].append(Item)
                print(L)
                return redirect(url_for('commercial',List=L.keys(),D=L))
        else:
                return redirect(url_for('index'))
                    

                
             

@app.route("/logout")
def logout():
	logout_user()
	sess['name']=None
	return redirect(url_for("login"))


@app.errorhandler(401)
def error1(error):
    return "<h1><center> Not Authorized</center></h1>"

if __name__=='__main__':
   app.run(debug=True)