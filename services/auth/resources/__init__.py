import config
import errors
from flask_restful import Api
from .auth import *
from .category import *
from .job import *
from .routes import initialize_routes

api = Api(prefix=config.API_PREFIX, errors=errors.errors)

initialize_routes(api)
