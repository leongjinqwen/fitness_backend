from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from flask_login import login_user,login_required,current_user,logout_user
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect(url_for('users.show',username=current_user.username))
    return render_template('sessions/new.html')


@sessions_blueprint.route('/login', methods=['POST'])
def create():
    password = request.form['password']
    user = User.get(User.email==request.form['email'])
    
    if user :
        check_password = check_password_hash(user.password,password)
        if check_password:
            login_user(user)
            flash("Successfully signed in.","primary")
            return redirect(url_for('users.show',username=user.username))
        else:
            flash("Password not matched","danger")
            return render_template('sessions/new.html',username=request.form['email'])
    else:
        return render_template('sessions/new.html',username=request.form['email'])

@sessions_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))



