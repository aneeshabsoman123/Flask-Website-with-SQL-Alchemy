from flask import Flask, render_template, request, url_for, redirect,flash  

from flask_wtf import Form  
from wtforms import validators, ValidationError  
from wtforms import TextAreaField, SubmitField, SelectField ,PasswordField,IntegerField
from wtforms.fields import TextField, BooleanField
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import StringField,  HiddenField
from wtforms.validators import Email, DataRequired
from email_validator import validate_email, EmailNotValidError

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

from urllib.parse import quote_plus


#configuring SQLAlchemy by setting a database URI and disabling tracking,
app = Flask(__name__)

key='aneesha!@1994'
app.config['SECRET_KEY']=key
password = quote_plus(key)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@20.246.105.39:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# store your database object in a variable called db
db = SQLAlchemy(app)



@app.route("/")
def index():
    return render_template("home.html")



@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')


@app.route('/about_me')
def about_me():
   return render_template('about_me.html')

@app.route('/nlp')
def nlp():
   return render_template('nlp.html')

@app.route('/articles')
def articles():
   return render_template('articles.html')

@app.route('/computer_vision')
def computer_vision():
   return render_template('computer_vision.html')

@app.route('/regression_classification')
def regression_classification():
   return render_template('regression_classification.html')

class ContactForm(FlaskForm):
   name = TextField("Whats is your User name?",[validators.Required("Please enter your name.")])
   #email=TextField("Whats is your email?",[validators.Required("Please enter your email")])
   submit = SubmitField("Send")


@app.route('/contact', methods = ['GET', 'POST'])  
def contact():  
   name=None
   form = ContactForm()  

   if form.validate_on_submit():
      name=form.name.data
      form.name.data=''
      flash('Form submitted successfully')
      
   return render_template('contact.html',name=name,form=form) 

   
  
@app.route('/success',methods = ['GET','POST'])  
def success():  
   return render_template("success.html")  

#use the database object to create a database table for User
#model — a Python class that inherits from a base class
#create a User model, which inherits from the db.Model class. This represents the user table
# db.Column class to define columns for your table
class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(20), nullable=False, unique=True)
      email = db.Column(db.String(30), nullable=False, unique=True)
      date_added=db.Column(db.DateTime, default= datetime.utcnow)
      
      def __repr__(self):
         return '<Name %r>' %self.name
      
class UserForm(FlaskForm):
   name = TextField("Whats is your User name?",[validators.Required("Please enter your name.")])
   email=TextField("Whats is your email?",[validators.Required("Please enter your email")])
   submit = SubmitField("Send")
      
      
@app.route('/user/add',methods=['GET','POST'])
def add_user():
   name=None
   form = UserForm()  

   if form.validate_on_submit():
      #finding if email is unique by querying the database
      user=User.query.filter_by(email=form.email.data).first()
      user_name=User.query.filter_by(name=form.name.data).first()
      #if unique pushing into db
      if user is None and user_name is None:
         user=User(name=form.name.data,email=form.email.data)
         db.session.add(user)
         db.session.commit()
      name=form.name.data
      form.name.data=''
      form.email.data=''
      flash('Form submitted successfully')
   db_users=User.query.order_by(User.date_added)
   return render_template('add_user.html',name=name,form=form,db_users=db_users) 



if __name__=="__main__":
   with app.app_context():
        # create database tables if they do not exist already
        db.create_all()
        # start the Flask development server using the run() method
   app.run(debug=True)
   