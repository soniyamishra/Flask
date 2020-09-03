from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY']='20930e1efbbfb61fe5563206e3731d511f29d4190d0256d9f1576974822823c7'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app) 
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True

app.config['MAIL_USERNAME'] = "stationeymanagerkjsieit@gmail.com"
app.config['MAIL_PASSWORD'] = 'hytrniyakdtuwgyh'

mail=Mail(app)


from flaskBlog import routes