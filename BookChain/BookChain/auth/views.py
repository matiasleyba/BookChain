from . import auth
from flask import render_template,session,redirect,flash,url_for
from BookChain.forms import LoginForm
from BookChain.firestore_service import get_user,user_put
from BookChain.models import UserData,UserModel
from flask_login import login_user, login_required ,logout_user 
from werkzeug.security import generate_password_hash,check_password_hash


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form=LoginForm()
    context = {
        'login_form' : login_form
        }

    if login_form.validate_on_submit():
         username = login_form.username.data
         password = login_form.password.data
         user_doc = get_user(username)
         if user_doc.to_dict() is not None:
             password_from_db = user_doc.to_dict()['password']

             if check_password_hash(user_doc.to_dict()['password'], password):
                 user_data = UserData(username,password)
                 user = UserModel(user_data)
                 login_user(user)
                 flash('Welcome',category='notice')
                 return redirect(url_for('index'))
                 
             else:
                 flash('Credentials error ')

         else : 
            flash('Credentials Fail')


         

         return redirect(url_for('index'))

    return render_template('login.html',**context)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form':signup_form    
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            passsword_hash = generate_password_hash(password)
            user_data = UserData(username,passsword_hash)
            
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Welcome')

            return redirect(url_for('index'))
        else:
            flash('User already exists')
    return render_template('signup.html',**context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bye')
    return redirect(url_for('auth.login'))

