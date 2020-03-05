"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,redirect,url_for
from BookChain import app,bootstrap
from BookChain.forms import LoginForm
import unittest
import wtforms

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html', error=error)


@app.route('/',methods=['GET'])
def home():
    """Renders the home page."""
    return redirect(url_for('auth.login'))

@app.route('/index',methods=['GET'])
def index():
    """Renders the index page."""
    return render_template(
        'index.html'
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        year=datetime.now().year
    )
if __name__ == '__main__':
    app.run(debug=True)

