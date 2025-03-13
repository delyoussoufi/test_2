from flask import Blueprint

# Create a new Blueprint here. You must register it in the flaskapp __init__.py after.
rest = Blueprint('rest', __name__)
admin = Blueprint('admin', __name__)
report = Blueprint('report', __name__)
users = Blueprint('users', __name__)
digitalisat = Blueprint('digitalisat', __name__)
vorgang = Blueprint('vorgang', __name__)
search_category = Blueprint('search_category', __name__)
digi = Blueprint('digi', __name__)
public = Blueprint('public', __name__)
sse = Blueprint('sse', __name__)

# import the controllers.
from flaskapp.controllers import user_controller, login_controller, vorgang_controller, \
    admin_controller, profile_controller, digi_connection_controller, \
    search_category_controller, digitalisat_controller, server_send_event_controller, public_controller
