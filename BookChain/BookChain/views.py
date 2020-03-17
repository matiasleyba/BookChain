"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,redirect,url_for,make_response,flash,request
from BookChain import app,bootstrap
from BookChain.forms import BookForm,SearchBoxForm,RequestForm ,EvaluateRequestForm
from BookChain.models import BookData, RequestData
from BookChain.Utils.Constants import Constants
import unittest
import wtforms

from BookChain.firestore_service import get_users ,get_books ,create_book,send_request,get_requests,get_request
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
    request_form = RequestForm()
    user = current_user.id
    if search_box_form.validate_on_submit():
        search = search_box_form.search.data
        books = get_books(search)
    else:
        books = get_books()

    if request_form.validate_on_submit():
        request_data= RequestData(request_form.book.data,user,request_form.comment.data)
        send_request(request_data)
        flash('Solicitud Enviada')

    context = {
        'books':books,
        'search_box_form':search_box_form,
        'request_form':request_form,
        'title':'Libros',
        'constants':Constants,
        'my_books':False
        }
    return render_template(
        'index.html' ,**context
    )

@app.route('/mybooks',methods=['GET','POST'])
@login_required
def mybooks():
    """Renders the index page."""
    search_box_form = SearchBoxForm()
    requests = get_requests()
    evaluate_request_form = EvaluateRequestForm()
    if search_box_form.validate_on_submit():
        search = search_box_form.search.data
        books = get_books(search,True)
    else:
        books = get_books(my_books=True)

    
    #request = get_request('3717pkg9ZlssEk5BCuqg')

    context = {
        'books':books,
        'get_request': get_request,
        'search_box_form':search_box_form,
        'evaluate_request_form':evaluate_request_form,
        'title':'Mis Libros',
        'constants':Constants,
        'my_books':True
    }
    return render_template(
        'books.html' ,**context
    )

@app.route('/newbook',methods=['GET','POST'])
@login_required
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
        flash('Libro creado')
        return redirect(url_for('index'))


    return render_template(
        'newbook.html',
        **context
    )

@app.route('/contact')
@login_required
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        year=datetime.now().year
    )


