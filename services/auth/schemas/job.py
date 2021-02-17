from ma import ma
from db import db
from models.job import JobModel
from models.category import CategoryModel


class UserJobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobModel
        load_only = ("category",)
        include_fk = True
        load_instance = True
        sqla_session = db.session


class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobModel
        dump_only = ("slug",)
        load_only = ("category",)
        include_fk = True
        load_instance = True
        sqla_session = db.session
