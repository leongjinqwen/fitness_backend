from flask import Blueprint,jsonify,request,make_response
from models.user import User
from models.message import Message
import os

messages_api_blueprint = Blueprint('messages_api',
							 __name__,
							 template_folder='templates')

@messages_api_blueprint.route('/<int:id>', methods=['POST'])
def create(id):
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
	sender = User.get(User.id == user_id) # find the current user(sender)
	receiver = User.get(User.id == id) # find the current user(receiver)
	if sender and receiver :
		post_data = request.get_json()
		message = Message(sender=sender.id,receiver=receiver.id,message=post_data['message'])
		if message.save():
			responseObject = {
				'status': 'success',
				'message': 'Record successfully saved.'
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

@messages_api_blueprint.route('show/<int:id>', methods=['GET'])
def show(id):
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
	sender = User.get(User.id == user_id) # find the current user(sender)
	receiver = User.get(User.id == id) # find the current user(receiver)
	if sender and receiver :
		messages = Message.select().where(Message.sender==sender.id,Message.receiver==receiver.id)
		conversation = []
		for message in messages:
			conversation.append(message.message)
		responseObject = {
			'status': 'success',
			'conversation': conversation
		}
		return make_response(jsonify(responseObject)), 200
	else:
		responseObject = {
			'status': 'failed',
			'message': 'Something happened,try again later.'
		}
		return make_response(jsonify(responseObject)), 401