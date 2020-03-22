from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField , SelectField ,TextAreaField ,BooleanField
from wtforms.validators import DataRequired ,Required
from BookChain.firestore_service import get_states

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class BookForm(FlaskForm):
    name = StringField('Nombre' , validators=[DataRequired()])
    description = StringField('Descripcion' , validators=[DataRequired()])
    genre = SelectField('Genero', validators=[DataRequired()])
    author = StringField('Autor',validators=[DataRequired()])
    lang = SelectField('Genero', validators=[DataRequired()])
    #state = SelectField('State', choices=[(state.id,state.to_dict()['value']) for state in get_states()], validators = [Required()])
    image_url = StringField('URL Portada')
    submit = SubmitField('Crear')

class SearchBoxForm(FlaskForm):
    search = StringField('Buscar')
    #submit = SubmitField('Enviar')
class RequestForm(FlaskForm):
    book = StringField('book',validators=[DataRequired()])
    comment = TextAreaField('Comentario',validators=[DataRequired()])
    submit = SubmitField('Enviar Solicitud')
class EvaluateRequestForm(FlaskForm):
    book = StringField('book',validators=[DataRequired()])
    owner_comment = TextAreaField('Comentario',validators=[DataRequired()]) 
    approved = SubmitField('Aprobar')
    denegated = SubmitField('Denegar')
    