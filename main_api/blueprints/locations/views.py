from flask import Blueprint, render_template, flash, redirect, url_for, request,jsonify
from models.position import Position
from models.user import User
import datetime

locations_api_blueprint = Blueprint('locations_api',
                             __name__,
                             template_folder='templates')


@locations_api_blueprint.route('/show', methods=['POST'])
def show():
    # get current_user location to show at center of map
    post_data = request.get_json()
    print(post_data)
    user = User.get_or_none(id=post_data.get('id'))
    current_location = Position.get(Position.user==user.id)
    locations = []
    # positions = (Position.select()
    #             .where(
    #                 Position.user!=user.id,
    #                 Position.updated_at+datetime.timedelta(minutes=180) > datetime.datetime.now()
    #             ))
    positions = (Position.select()
                .where(
                    Position.updated_at+datetime.timedelta(minutes=180) > datetime.datetime.now()
                ))
    for position in positions:
        locations.append({
            'user' : position.user.username,
            'position' : {'lat':float(position.lat),'lng':float(position.lng)}
        })
    return jsonify({
        'ok': True,
        'locations': locations,
        'current_user':user.username,
        'current_location_lat':float(current_location.lat),
        'current_location_lng':float(current_location.lng)
    })

@locations_api_blueprint.route('/new', methods=['POST'])
def new():
    post_data = request.get_json()
    lat = post_data.get('lat')
    lng = post_data.get('lng')
    user = User.get_or_none(id=post_data.get('id'))
    position = Position.get_or_none(Position.user==user.id)

    if position == None :
        Position.create(user=user.id,lat=lat,lng=lng)
        return jsonify({
            'ok': True,
            'message': 'Position has been saved'
        })

    else:
        position.lat = lat
        position.lng = lng
        if not position.save():
            resp = jsonify({
                'message': 'Unable to save position'
            })
            resp.status_code = 400
            return resp
        return jsonify({
            'ok': True,
            'message': 'Position has been saved'
        })
