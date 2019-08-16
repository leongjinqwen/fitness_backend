from flask import Blueprint, render_template, flash, redirect, url_for, request,jsonify
from models.position import Position
from flask_login import current_user
import datetime

locations_blueprint = Blueprint('locations',
                            __name__,
                            template_folder='templates')


@locations_blueprint.route('/', methods=['GET'])
def new():
    # to show all online user location on map
    return render_template('locations/new.html')


@locations_blueprint.route('/show', methods=['GET'])
def show():
    # get current_user location to show at center of map
    current_location = Position.get(Position.user==current_user.id)
    locations = []
    positions = (Position.select()
                .where(
                    Position.user!=current_user.id,
                    Position.updated_at+datetime.timedelta(minutes=15) > datetime.datetime.now()
                ))
    for position in positions:
        locations.append({
            'user' : position.user.username,
            'position' : {'lat':float(position.lat),'lng':float(position.lng)}
        })
    return jsonify({
        'ok': True,
        'locations': locations,
        'current_user':current_user.username,
        'current_location_lat':float(current_location.lat),
        'current_location_lng':float(current_location.lng)
    })

@locations_blueprint.route('/create',methods=['POST'])
def create():
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    position = Position.get_or_none(Position.user==current_user.id)

    if position == None :
        Position.create(user=current_user.id,lat=lat,lng=lng)
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
