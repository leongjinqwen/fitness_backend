from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from models.image import Image
from flask_login import login_user,login_required,current_user
from main_web.util.helpers import upload_file_to_s3
import os
from models.relationship import Relationship

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['password']
    user = User(username=request.form['username'].lower(),email=request.form['email'].lower(),password=user_password)
    if user.save():
        login_user(user)
        flash("Successfully signed up and logged in.","primary")
        return redirect(url_for('users.show',username=user.username))
    else:
        return render_template('users/new.html',username=request.form['username'], errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username==username)
    if not current_user.is_authenticated:
        followed = None
    else:
        followed = Relationship.get_or_none(Relationship.fan==current_user.id,Relationship.idol==user.id)
    return render_template('users/show.html',user=user,followed=followed)


@users_blueprint.route('/', methods=["GET"])
def index():
    if current_user.is_authenticated:

        idols = (Relationship.select(Relationship.idol)
                .where( Relationship.fan == current_user.id, Relationship.approved == True)
                )
        images = (Image.select()
                .where((Image.user.in_(idols)) | (Image.user == current_user.id))
                .order_by(Image.created_at.desc()))

        return render_template('users/index.html',images=images)
    else:

        return render_template('sessions/new.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    return render_template('users/edit.html',user=user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    if current_user.id==user.id:
        print(current_user.id)
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        if not request.form.get('private'):
            user.private = False
        else:
            user.private = True
        if user.save():
            flash("Successfully updated.","primary")
            return redirect(url_for('users.edit',id=id))
        else:
            return render_template('users/edit.html',errors=user.errors,user=user)
    else:
        return render_template('users/edit.html', user=user)
  
@users_blueprint.route('/search', methods=["POST"])
def search():
    username = request.form['search'].lower()
    return redirect(url_for('users.show',username=username))