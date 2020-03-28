from flask_login import UserMixin
from BookChain.firestore_service import get_user
class UserData:
    def __init__(self,username,password,name,last_name,contact):
        self.username = username 
        self.password = password
        self.name  = name
        self.last_name = last_name
        self.contact = contact


class UserModel(UserMixin):
    def __init__(self,user_data):
        self.id = user_data.username
        self.password = user_data.password
        self.name  = user_data.username
        self.last_name = user_data.last_name
        self.contact = user_data.contact

    @staticmethod
    def query(user_id):
        user_doc =get_user(user_id)
        user_data = UserData(
            username = user_doc.id,
            password = user_doc.to_dict()['password'],
            name = user_doc.to_dict()['name'],
            last_name = user_doc.to_dict()['last_name'],
            contact = user_doc.to_dict()['contact']
        )

        return UserModel(user_data)


class BookData():
    def __init__(self,data,user):
        self.name= data['name'] 
        self.description = data['description']
        self.page_count= data['page_count'] 
        self.author = data['author']
        self.genre = data['genre']
        self.url_image = data['image_url']
        self.user = user
class RequestData():
    def __init__(self,book_id,user,days,comment):
        self.user=user
        self.book_id=book_id
        self.days = days
        self.comment=comment
    