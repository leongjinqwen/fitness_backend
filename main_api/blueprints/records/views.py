from flask import Blueprint,jsonify,request,make_response
from werkzeug.security import check_password_hash
from models.user import User
import os
import requests

records_api_blueprint = Blueprint('records_api',
                             __name__,
                             template_folder='templates')

@records_api_blueprint.route('/', methods=['GET'])
def get_record():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
		user_id = User.decode_auth_token(auth_token)
		user = User.get(User.id==user_id)
		from models.record import Record
		records = Record.select().where(Record.user==user.id).order_by(Record.id.asc())
		chart = []
		chartBmi = []
		result = []
		for record in records:
			chart.append([
				str(record.created_at.strftime('%d-%m-%Y')),record.weight
			])
			chartBmi.append([
				str(record.created_at.strftime('%d-%m-%Y')),record.bmi
			])
			result.append({
				'date':record.created_at.strftime('%d-%m-%Y'),
				'weight':record.weight,
				'height':record.height,
				'bmi':record.bmi,
			})
		responseObject = {
			'age': user.age,         
			'sex': user.sex,                
			'records' : result,
			'chart':chart,     
			'chartBmi':chartBmi     
		}
		return make_response(jsonify(responseObject)),200
	else:
		responseObject = {
			'status': 'failed',
			'message': 'No authorization header found.'
		}
		return make_response(jsonify(responseObject)), 401
	
@records_api_blueprint.route('/<int:id>', methods=['POST'])
def record(id):
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
	from models.record import Record
	if (user_id == id) and user :
		post_data = request.get_json()
		record = Record(weight=post_data['weight'],height=post_data['height'],bmi=post_data['bmi'],user=user.id)
		if record.save():
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

@records_api_blueprint.route('/nutrition', methods=['POST'])
def nutrition():
	import json
	from bs4 import BeautifulSoup
	post_data = request.get_json()
	concepts = post_data.get('concepts')
	results = []
	apikey = os.getenv('WOLFRAM_ID')
	for concept in concepts:
		r = requests.get(f"http://api.wolframalpha.com/v2/query?input={concept}%20nutrition%20facts&appid={apikey}")
		data = r.text
		check = []
		soup = BeautifulSoup(data,'html.parser')
		for img in soup.find_all('img'):
			if img:
				image = img['src']
				check.append(image)
		
		if check == []:
			results.append({'concept':concept,'image':'http://www5b.wolframalpha.com/Calculate/MSP/MSP1047318acidc2baiffa84000059cb2eif40h33712?MSPStoreType=image/gif&s=37'})
		else:
			results.append({'concept':concept,'image':check[1]})
		
	responseObject = {
		'status': 'success',
		'data': results
	}
	return make_response(jsonify(responseObject)), 201