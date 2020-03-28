from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField , SelectField ,TextAreaField ,BooleanField,IntegerField
from wtforms.validators import DataRequired ,Required
from wtforms.fields.html5 import EmailField
from flask.ext.wtf import Form
from wtforms import validators
from BookChain.firestore_service import get_states

class LoginForm(FlaskForm):
    username = StringField('Email de Usuario', validators=[DataRequired()])
    #username = EmailField('Email de usuario', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SignupForm(FlaskForm):
    username = StringField('Email de Usuario', validators=[DataRequired()])
    #username = EmailField('Email de usuario', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    last_name = StringField('Apellido', validators=[DataRequired()])
    contact = StringField('Telefono',validators=[DataRequired()])
    submit = SubmitField('Enviar')

class BookForm(FlaskForm):
    name = StringField('Nombre' , validators=[DataRequired()])
    description = StringField('Descripcion' , validators=[DataRequired()])
    page_count = IntegerField('Cantidad de paginas' , validators=[DataRequired()])
    genre = SelectField('Genero', validators=[DataRequired()])
    author = StringField('Autor',validators=[DataRequired()])
    lang = SelectField('Idioma', validators=[DataRequired()])
    image_url = StringField('URL Portada')
    submit = SubmitField('Crear')

class SearchBoxForm(FlaskForm):
    search = StringField('Buscar')
    #submit = SubmitField('Enviar')
class RequestForm(FlaskForm):
    book = StringField('book',validators=[DataRequired()])
    days = IntegerField('Cantidad de dias',validators=[DataRequired()])
    comment = TextAreaField('Comentario',validators=[DataRequired()])
    submit = SubmitField('Enviar Solicitud')
class EvaluateRequestForm(FlaskForm):
    book = StringField('book',validators=[DataRequired()])
    owner_comment = TextAreaField('Comentario',validators=[DataRequired()])
    #contact = StringField('Descripcion de contacto del propietario del libro',validators=[DataRequired()])
    user = StringField('Usuario que solicito el libro',validators=[DataRequired()])
    reputation = IntegerField('Reputacion',validators=[DataRequired()])
    approved = SubmitField('Aprobar')
    denegated = SubmitField('Denegar')
    