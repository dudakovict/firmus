import errors
from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .user import *
from .job import JobSchema
from .category import CategorySchema
