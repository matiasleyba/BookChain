"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
from BookChain.sendmail import EmailController
from flask import render_template,redirect,url_for,make_response,flash,request
from BookChain import app,bootstrap
from BookChain.forms import BookForm,SearchBoxForm,RequestForm ,EvaluateRequestForm
from BookChain.models import BookData, RequestData
from BookChain.Utils.Constants import Constants
import unittest
import wtforms

from BookChain.firestore_service import get_users ,get_books ,create_book,send_request,get_requests,get_request , denegate_request,approve_request,get_genres,get_langs,get_lang,get_genre,delivered_request
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
    #EmailController.SendEmail()
    
    search_box_form = SearchBoxForm()
    request_form = RequestForm()
    user = current_user.id
    if search_box_form.validate_on_submit():
        search = search_box_form.search.data
        books = get_books(search)
    else:
        books = get_books()


    context = {
        'books':books,
        'search_box_form':search_box_form,
        'get_genre':get_genre,
        'get_lang':get_lang,
        'request_form':request_form,
        'title':'Libros Disponibles',
        'constants':Constants,
        'my_books':False,
        'requested_books':False
        }
    if request_form.validate_on_submit():
        request_data= RequestData(request_form.book.data,user,request_form.days.data,request_form.comment.data)
        send_request(request_data)
        #mandar mail
        flash('Solicitud Enviada , se notificara al propietario.')
        response = make_response(redirect('/index'))
        return response
        #return render_template('index.html' ,**context)
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
        books = get_books(search,my_books=True)
    else:
        books = get_books(my_books=True)

    if evaluate_request_form.validate_on_submit():
        if evaluate_request_form.approved.data:
            approve_request(evaluate_request_form.request_id.data,evaluate_request_form.owner_comment.data)
            flash('La solicitud fue aprobada , ahora puedes ver los datos del solicitante y coordinar la entrega del libro.Cuando entregues el libro marca el libro como entregado.')
            flash('Cuando entregues el libro marca el libro como entregado.')
            response = make_response(redirect('/mybooks'))
            return response
        elif evaluate_request_form.denegated.data:
            denegate_request(evaluate_request_form.book.data)
            flash('Prestamo Rechazado')
            response = make_response(redirect('/mybooks'))
            return response
        else:
            delivered_request(evaluate_request_form.book.data)
            flash('Se marco el libro como entregado , gracias por colaborar !')
            response = make_response(redirect('/mybooks'))
            return response



        
    
    #request = get_request('3717pkg9ZlssEk5BCuqg')

    context = {
        'books':books,
        'get_request': get_request,
        'get_genre':get_genre,
        'get_lang':get_lang,
        'search_box_form':search_box_form,
        'evaluate_request_form':evaluate_request_form,
        'title':'Mis Libros - Registrados',
        'constants':Constants,
        'my_books':True,
        'requested_books':False
    }
    return render_template(
        'books.html' ,**context
    )

@app.route('/requested-books',methods=['GET','POST'])
@login_required
def requested_books():
    """Renders the index page."""
    search_box_form = SearchBoxForm()
    requests = get_requests()
    evaluate_request_form = EvaluateRequestForm()
    if search_box_form.validate_on_submit():
        search = search_box_form.search.data
        books = get_books(search,requested_books=True)
    else:
        books = get_books(requested_books=True)

           
    #request = get_request('3717pkg9ZlssEk5BCuqg')

    context = {
        'books':books,
        'get_request': get_request,
        'get_genre':get_genre,
        'get_lang':get_lang,
        'search_box_form':search_box_form,
        'evaluate_request_form':None,
        'title':'Mis Libros - Solicitados',
        'constants':Constants,
        'my_books':True,
        'requested_books':True
    }
    return render_template(
        'requested-books.html' ,**context
    )

@app.route('/newbook',methods=['GET','POST'])
@login_required
def newbook():
    """Renders the contact page."""
    book_form=BookForm()
    user = current_user.id
    genres = get_genres()
    langs = get_langs()
    book_form.genre.choices = [(g.id, g.to_dict()['name']) for g in genres]
    book_form.lang.choices = [(g.id, g.to_dict()['name']) for g in langs]
    context = {
        'book_form' : book_form
        }
    if book_form.validate_on_submit():
        #book_data = BookData(book_form.data,user)
        create_book(book_form.data,user)
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


