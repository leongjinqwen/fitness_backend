from flask import Blueprint,jsonify,make_response,request
from models.user import User
from werkzeug.security import generate_password_hash
import string
from random import *
import datetime
import os
import requests

users_api_blueprint = Blueprint('users_api',
									  __name__,
									  template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
	users = User.select()
	result = []
	for user in users:
		each = {
			'id': user.id,
			'username': user.username,
			'email': user.email,
			'age': user.age,
			'sex': user.sex,
			'profile_pic': user.profile_image_url,
			'description': user.description
		}
		result.append(each)
	return jsonify(result)

@users_api_blueprint.route('/new', methods=['POST'])
def create():
	post_data = request.get_json()
	try:
		new_user = User(
			username=post_data['username'],
			email=post_data['email'].lower(),
			password=post_data['password'],
			age=post_data['age'],
			sex=post_data['sex'],
			description=post_data['description'],
		)
	except:
		responseObject = {
			'status': 'failed',
			'message': ['All fields are required!']
		}
		return make_response(jsonify(responseObject)), 400

	else:
		if not new_user.save():
			responseObject = {
				'status': 'failed',
				'message': new_user.errors
			}
			return make_response(jsonify(responseObject)), 400
		else:
			auth_token = new_user.encode_auth_token(new_user.id)
			responseObject = {
				'status': 'success',
				'message': 'Successfully created a user and signed in.',
				'auth_token': auth_token.decode(),
				'user': {
					'id': new_user.id,
					'username': new_user.username,
					'email': new_user.email,         
					'age': new_user.age,         
					'sex': new_user.sex,                
					'description': new_user.description,         
				}
			}
			return make_response(jsonify(responseObject)), 201

@users_api_blueprint.route('/me', methods=['GET'])
def currentuser():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
		user_id = User.decode_auth_token(auth_token)
		user = User.select().where(User.id==user_id)
		responseObject = {
			'id': user[0].id,
			'username': user[0].username,
			'email': user[0].email,         
			'age': user[0].age,         
			'sex': user[0].sex,                
			'description': user[0].description,         
		}
		return make_response(jsonify(responseObject)),201
	else:
		responseObject = {
			'status': 'failed',
			'message': 'No authorization header found.'
		}
		return make_response(jsonify(responseObject)), 401


@users_api_blueprint.route('/edit/<int:id>', methods=['POST'])
def edit(id):
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
	else:
		responseObject = {
			'status': 'failed',
			'message': 'No authorization header found.'
		}
		return make_response(jsonify(responseObject)), 401

	user_id = User.decode_auth_token(auth_token)
	user = User.get(User.id == user_id)
	if (user_id == id) and user :
		post_data = request.get_json()
		user.username = post_data['username']
		user_password = post_data['password']
		user.password = user_password
		user.sex = post_data['sex']
		user.age = post_data['age']
		user.description = post_data['description']
		if user.save():
			responseObject = {
				'status': 'success',
				'message': 'Profile successfully updated.'
			}
			return make_response(jsonify(responseObject)), 201
		else:
			responseObject = {
				'status': 'failed',
				'message': 'Something happened,try again later.'
			}
			return make_response(jsonify(responseObject)), 400
	else:
		responseObject = {
			'status': 'failed',
			'message': 'Authentication failed'
		}
		return make_response(jsonify(responseObject)), 401

@users_api_blueprint.route('/reset', methods=["POST"])
def reset_password():
	post_data = request.get_json()
	user = User.get(User.email==post_data['email'])
	min_char = 8
	max_char = 12
	allchar = string.ascii_letters + string.punctuation + string.digits
	user_password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
	user.password = user_password
	if user.save():
		responseObject = {
			'status': 'success',
			'message': 'New password successfully sent to your email.'
		}
		return make_response(jsonify(responseObject)), 201
	else:
		responseObject = {
			'status': 'failed',
			'message': 'Something happened,try again later.'
		}
		return make_response(jsonify(responseObject)), 400

@users_api_blueprint.route('/delete', methods=['POST'])
def delete():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
	else:
		responseObject = {
			'status': 'failed',
			'message': 'No authorization header found.'
		}
		return make_response(jsonify(responseObject)), 401

	user_id = User.decode_auth_token(auth_token)
	user = User.delete().where(User.id == user_id)
	if user.execute():
		responseObject = {
			'status': 'success',
			'message': 'Account successfully deleted.'
		}
		return make_response(jsonify(responseObject)), 201
	else:
		responseObject = {
			'status': 'failed',
			'message': 'Something happened,try again later.'
		}
		return make_response(jsonify(responseObject)), 400

