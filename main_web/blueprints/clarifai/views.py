from app import app
from flask import Blueprint, render_template, flash, redirect, url_for, request,jsonify

clarifai_blueprint = Blueprint('clarifai',
                            __name__,
                            template_folder='templates')


@clarifai_blueprint.route('/', methods=['GET'])
def new():
    return render_template('clarifai/new.html')

@clarifai_blueprint.route('/show', methods=['GET'])
def show():
    return render_template('clarifai/body.html')