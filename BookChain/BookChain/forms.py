from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField , SelectField
from wtforms.validators import DataRequired ,Required
from BookChain.firestore_service import get_states

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class BookForm(FlaskForm):
    name = StringField('Book Name' , validators=[DataRequired()])
    description = StringField('Book Description' , validators=[DataRequired()])
    #state = SelectField('State', choices=[(state.id,state.to_dict()['value']) for state in get_states()], validators = [Required()])
    submit = SubmitField('Crear')

class SearchBoxForm(FlaskForm):
    search = StringField('Buscar')
    #submit = SubmitField('Enviar')