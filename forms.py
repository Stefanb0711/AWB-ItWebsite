from flask_ckeditor import CKEditorField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import DataRequired, Email

from wtforms import StringField, SubmitField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    phone_number = IntegerField('Telefon', validators=[DataRequired()])
    mobile_phone_number = IntegerField('Mobil', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired("Füllen Sie die Felder aus"), Email("This field requires a valid email address")])
    question = StringField('Wie können wir ihnen helfen', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BlogPostForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    subtitle = StringField('Untertitel', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    post = SubmitField('Posten')

