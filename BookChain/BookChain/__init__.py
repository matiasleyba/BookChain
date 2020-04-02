"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from BookChain.auth import auth
from flask_login import LoginManager
from BookChain.models import UserModel
from flask_assets import Environment, Bundle

login_manager = LoginManager()
login_manager.login_view ='auth.login'

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

app = Flask(__name__)
assets = Environment(app)
assets.url = app.static_url_path
assets.debug = True

scss = Bundle('scss/rating.scss', filters='pyscss', output='gen/all.css')
assets.register('scss_all', scss)

bootstrap = Bootstrap(app)
login_manager.init_app(app)
app.register_blueprint(auth)
import BookChain.views

