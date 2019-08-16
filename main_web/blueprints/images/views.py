from flask import Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from models.image import Image
from flask_login import login_required,current_user
from main_web.util.helpers import upload_file_to_s3
import os

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
def create():
    if "user_file" not in request.files:
        flash("No user_file key in request.files",'danger')
        return redirect(url_for('images.new'))

    file = request.files["user_file"]
    
    if file:
        output = upload_file_to_s3(file, os.environ.get("S3_BUCKET_NAME"))
        image = Image(image_path = str(output),user = current_user.id)
        if image.save():
            flash("Photo successfully uploaded.",'primary')
            return redirect(url_for('images.new'))
    else:
        return render_template('home.html')

@images_blueprint.route('/<username>', methods=['GET'])
def show(username):
    user = User.get(User.username==username)
    images = Image.select().where(Image.user==user)
    return render_template('images/show.html',user=user,images=images)


