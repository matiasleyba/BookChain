import firebase_admin
from flask import url_for
from firebase_admin import credentials
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
    user_ref.set({'password': user_data.password})

def get_states():
    return db.collection('States').get()

def get_state_available():
    states = db.collection('States')
    query = states.where(u'value', u'==', u'Disponible')
    docs = query.stream()
    doc = list(docs)[0]
    return doc

def get_books(filter=''):
    if(filter==''):
        return db.collection('Books').get()
    else:
        books = db.collection('Books')
        #query = books.order_by('name').start_at(filter).end_at(filter+'\uf8ff').get()
        query = books.where(u'name', u'==', filter).get()
        return query
    

def create_book(book_data):
    book_ref=db.collection('Books').document()
    state = get_state_available()
    book_ref.set({'name':book_data.name , 'description':book_data.description , 'state': state.id , 'user':book_data.user})





