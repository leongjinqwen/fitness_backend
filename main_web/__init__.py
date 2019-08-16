from app import app
from flask import render_template
from main_web.blueprints.users.views import users_blueprint
from main_web.blueprints.sessions.views import sessions_blueprint
from main_web.blueprints.images.views import images_blueprint
from main_web.blueprints.fanidols.views import fanidols_blueprint
from main_web.blueprints.locations.views import locations_blueprint
from main_web.blueprints.clarifai.views import clarifai_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from .util.jinja_filter import register_jinja_filters

assets = Environment(app)
register_jinja_filters(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(fanidols_blueprint, url_prefix="/fanidols")
app.register_blueprint(locations_blueprint, url_prefix="/locations")
app.register_blueprint(clarifai_blueprint, url_prefix="/clarifai")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
