from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from webApplication import db
from webApplication.scripts.db_models import user_accounts
from  werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['POST', 'GET'])
@auth.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        _username = request.form.get('username')
        _password = request.form.get('password')

        user = user_accounts.query.filter_by(username=_username).first()
        
        if user: 
            if check_password_hash(user.password, _password):
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash(' Password is incorrect! ', category='error')
        else:
            flash('Email does not exist', category='error')
        
        return redirect(url_for('.login'))

    else:
        return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        _username = request.form.get('username')
        _password = request.form.get('password')

        user = user_accounts.query.filter_by(username=_username).first()

        if user == None:
            if len(_username) < 5:
                flash('Username must be at least 5 characters', category='error')
            elif len(_password) < 5:
                flash('Password must be at least 5 characters', category='error')
            else:
                new_account = user_accounts(username=_username, password=generate_password_hash(_password, method="sha256"))
                db.session.add(new_account)
                db.session.commit()
                flash('Account created successfully!', category='success')
        else:
            flash('User account already existing', category='error')

        return redirect(url_for('.register'))
    else:
        return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))