"""
The flask application package.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from BookChain.auth import auth

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.register_blueprint(auth)
import BookChain.views

