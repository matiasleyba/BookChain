import firebase_admin
from flask import url_for
from firebase_admin import credentials
from flask_login import current_user

from firebase_admin import firestore
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'firestore/bookchain-flask-firebase-adminsdk-qzuco-2c4b92bd49.json')
cred = credentials.Certificate(filename)
firebase_admin.initialize_app(cred)
db = firestore.client()

#if (not len(firebase_admin._apps)):
  #cred = credentials.ApplicationDefault()
 # firebase_admin.initialize_app(cred, {
  #  'projectId': 'bookchain-flask',
  #})

#db = firestore.client()


def get_users():
    return db.collection('Users').get()

def get_user(user_id):
    return db.collection('Users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('Users').document(user_data.username)
    user_ref.set({'password': user_data.password , 'name':user_data.name , 'last_name':user_data.last_name , 'contact': user_data.contact})

def get_states():
    return db.collection('States').get()

def get_state_available():
    states = db.collection('States')
    query = states.where(u'value', u'==', u'Disponible')
    docs = query.stream()
    doc = list(docs)[0]
    return doc
def get_genres():
    genres_ref=db.collection('Genres').get()
    docs = list(genres_ref)
    return docs
def get_genre(genre):
    genre_ref = db.document('Genres/{}'.format(genre.id)).get()
    return genre_ref.to_dict()['name']
def get_langs():
    langs_ref=db.collection('Langs').get()
    docs = list(langs_ref)
    return docs
def get_lang(lang):
    lang_ref = db.document('Langs/{}'.format(lang.id)).get()
    return lang_ref.to_dict()['name']
def get_books(filter='',my_books=False,requested_books=False):
    user = current_user
    #singleton
    query = db.collection('Books')
    docs = list(query.get())

    if(filter!=''):
        docs = [s for s in docs if filter.lower() in s.to_dict()['name'].lower()]
       

    if(my_books==True):
        docs = [x for x in docs if x.to_dict()['user'].id == user.id]
    elif (requested_books==True):
        docs = [x for x in docs if (x.to_dict()['user'].id != user.id and x.to_dict()['state'].id=='loaned' or x.to_dict()['state'].id=='requested')]
    else:
        docs = [x for x in docs if (x.to_dict()['user'].id != user.id and x.to_dict()['state'].id=='available')]
    return docs
    

def create_book(book_data,user):
    book_ref=db.collection('Books').document()
    state = db.document('States/available')
    genre = db.document('Genres/{}'.format(book_data['genre']))
    lang= db.document('Langs/{}'.format(book_data['lang']))
    user = db.document('Users/{}'.format(user))
    book_ref.set(book_data)
    book_ref.update({'lang':lang,'genre':genre,'state': state , 'user':user})

def send_request(request_data):
    request_ref=db.collection('Requests').document()
    user = db.collection('Users').document(request_data.user)
    book = db.collection('Books').document(request_data.book_id)
    state = db.document('States/requested')
    request_ref.set({'book':book,'user':user,'days':request_data.days,'comment':request_data.comment,'send_email':False,'owner_comment':''})
    book.update({'state':state})

def get_requests():
    request_ref=db.collection('Requests').get()
    docs = list(request_ref)
    docs.sort(key=lambda x: x.create_time.seconds, reverse=True)
    #next((i.to_dict()['comment'] for i in requests if i.to_dict()['book'].id == '3717pkg9ZlssEk5BCuqg'),None)
    return docs
def get_request(book_id):
    request_ref=db.collection('Requests')
    book = db.collection('Books').document(book_id)
    query = request_ref.where('book', '==', book)
    #docs = query.stream()
    docs = list(query.get())
    docs.sort(key=lambda x: x.create_time.seconds, reverse=True)
    user = db.collection('Users').document(list(docs)[0].to_dict()['user'].id).get()
    try:
        request = {
            'comment':list(docs)[0].to_dict()['comment'],
            'days':list(docs)[0].to_dict()['days'],
            'send_email':list(docs)[0].to_dict()['send_email'],
            'id':list(docs)[0].id,
            'owner_comment':list(docs)[0].to_dict()['owner_comment'],
            'user':user
        }
        return request
    except IndexError:
        return ''

def approve_request(request_id,owner_comment):
    request_ref=db.collection('Requests').document(request_id)
    request_ref.update({'send_email':True,'owner_comment':owner_comment})
    #mail
def denegate_request(book_id):
    book = db.collection('Books').document(book_id)
    state = db.document('States/available')
    book.update({'state':state})
def delivered_request(book_id):
    book = db.collection('Books').document(book_id)
    state = db.document('States/loaned')
    book.update({'state':state})
    
  



