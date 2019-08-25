import os
from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from main_api.blueprints.users.views import users_api_blueprint
from main_api.blueprints.sessions.views import sessions_api_blueprint
from main_api.blueprints.locations.views import locations_api_blueprint
from main_api.blueprints.records.views import records_api_blueprint
from main_api.blueprints.messages.views import messages_api_blueprint



app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/')
app.register_blueprint(locations_api_blueprint, url_prefix='/api/v1/locations')
app.register_blueprint(records_api_blueprint, url_prefix='/api/v1/records')
app.register_blueprint(messages_api_blueprint, url_prefix='/api/v1/messages')


