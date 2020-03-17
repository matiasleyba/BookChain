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
    user_ref.set({'password': user_data.password})

def get_states():
    return db.collection('States').get()

def get_state_available():
    states = db.collection('States')
    query = states.where(u'value', u'==', u'Disponible')
    docs = query.stream()
    doc = list(docs)[0]
    return doc

def get_books(filter='',my_books=False):
    user = current_user
    #singleton
    query = db.collection('Books')
    docs = list(query.get())

    if(filter!=''):
        docs = [s for s in docs if filter.lower() in s.to_dict()['name'].lower()]
       

    if(my_books==False):
        docs = [x for x in docs if (x.to_dict()['user'] != user.id and x.to_dict()['state'].id=='available')]
    else:
        docs = [x for x in docs if x.to_dict()['user'] == user.id]
    
    return docs
    

def create_book(book_data):
    book_ref=db.collection('Books').document()
    state = db.document('States/available')
    book_ref.set({'name':book_data.name , 'description':book_data.description , 'state': state , 'user':book_data.user})

def send_request(request_data):
    request_ref=db.collection('Requests').document()
    user = db.collection('Users').document(request_data.user)
    book = db.collection('Books').document(request_data.book_id)
    state = db.document('States/requested')
    request_ref.set({'book':book,'user':user,'comment':request_data.comment})
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
    try:
        print(list(docs)[0].to_dict()['comment'])
        return list(docs)[0].to_dict()['comment']
    except IndexError:
        return ''
    
  



