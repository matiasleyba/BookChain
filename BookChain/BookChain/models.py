from flask_login import UserMixin
from BookChain.firestore_service import get_user
class UserData:
    def __init__(self,username,password):
        self.username = username 
        self.password = password



class UserModel(UserMixin):
    def __init__(self,user_data):
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc =get_user(user_id)
        user_data = UserData(
            username = user_doc.id,
            password = user_doc.to_dict()['password']
        )

        return UserModel(user_data)


class BookData():
    def __init__(self,name,description,user):
        self.name= name 
        self.description = description
        self.state= 'Disponible'
        self.user = user
class RequestData():
    def __init__(self,book_id,user,comment):
        self.user=user
        self.book_id=book_id
        self.comment=comment
    