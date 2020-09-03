from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskBlog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=12)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Comfirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')
    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose a different one')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already exist. Please register with different email')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=12)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Update')
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    def validate_username(self,username):
        if(current_user.username!=username.data):
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose a different one')
    
    def validate_email(self,email):
        if(current_user.email!=email.data):
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already exist. Please register with different email')

class RequestResestForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email is does not exist. Please register with different email')


class ResetPasswordForm(FlaskForm):
    password=PasswordField(validators=[DataRequired()])
    confirm_password=PasswordField(validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Reset Password')