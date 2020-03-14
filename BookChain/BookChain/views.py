"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,redirect,url_for,make_response,flash,request
from BookChain import app,bootstrap
from BookChain.forms import BookForm,SearchBoxForm
from BookChain.models import BookData
import unittest
import wtforms

from BookChain.firestore_service import get_users ,get_books ,create_book
from flask_login import login_required ,current_user
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
    
    response = make_response(redirect('/index'))
    return response

@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    """Renders the index page."""
    search_box_form = SearchBoxForm()

    if search_box_form.validate_on_submit():
        search = search_box_form.search.data
        books = get_books(search)
    else:
        books = get_books()

    context = {
        'books':books,
        'search_box_form':search_box_form
        }
    return render_template(
        'index.html' ,**context
    )
@app.route('/newbook',methods=['GET','POST'])
def newbook():
    """Renders the contact page."""
    book_form=BookForm()
    user = current_user.id
    context = {
        'book_form' : book_form
        }
    if book_form.validate_on_submit():
        book_data = BookData(book_form.name.data,book_form.description.data,user)
        create_book(book_data)
        flash('Book creado')
        return redirect(url_for('index'))

    return render_template(
        'newbook.html',
        **context
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        year=datetime.now().year
    )


