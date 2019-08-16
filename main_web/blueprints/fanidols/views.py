from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from models.relationship import Relationship
from flask_login import current_user
import os

fanidols_blueprint = Blueprint('fanidols',
                            __name__,
                            template_folder='templates')


@fanidols_blueprint.route('/<id>/create', methods=['POST'])
def create(id):
    idol = User.get_by_id(id)
    if idol.private == True:
        relationship = Relationship(fan=current_user.id,idol=idol.id,approved=False)
        if relationship.save():
            flash(f"Request is sent to {idol.username}. Please wait for approval.","primary")
            return redirect(url_for('users.show',username=idol.username))
    else:
        relationship = Relationship(fan=current_user.id,idol=idol.id,approved=True)
        if relationship.save():
            flash(f"Successfully followed {idol.username}.","primary")
            return redirect(url_for('users.show',username=idol.username))

@fanidols_blueprint.route('/<id>/delete', methods=['POST'])
def delete(id):
    idol = User.get_by_id(id)
    relationship = Relationship.delete().where(Relationship.fan==current_user.id,Relationship.idol==idol.id)
    relationship.execute()
    flash(f"Successfully unfollowed {idol.username}.","primary")
    return redirect(url_for('users.show',username=idol.username))

@fanidols_blueprint.route('/',methods=['GET'])
def show():
    followers = Relationship.select().where(Relationship.idol==current_user.id,Relationship.approved==False)
    return render_template('fanidols/show.html',followers=followers)

@fanidols_blueprint.route('/<id>/approved',methods=['POST'])
def approved(id):
    fan = User.get_by_id(id)
    follower = Relationship.update(approved=True).where(Relationship.fan==id,Relationship.idol==current_user.id)
    if follower.execute():
        flash(f'{fan.username} now is your follower.','primary')
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash(f'Failed to approve request,try again later.','danger')
        return render_template('fanidols/show.html')

@fanidols_blueprint.route('/<id>/reject',methods=['POST'])
def reject(id):
    fan = User.get_by_id(id)
    follower = Relationship.delete().where(Relationship.fan==id,Relationship.idol==current_user.id)
    if follower.execute():
        flash(f"You reject {fan.username}'s following request.",'primary')
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash(f'Failed to approve request,try again later.','danger')
        return render_template('fanidols/show.html')
