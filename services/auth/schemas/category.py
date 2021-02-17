from ma import ma
from db import db
from models.category import CategoryModel
from models.job import JobModel
from schemas.job import JobSchema


class CategorySchema(ma.SQLAlchemyAutoSchema):
    jobs = ma.Nested(JobSchema, many=True)

    class Meta:
        model = CategoryModel
        dump_only = ("slug",)
        include_fk = True
        load_instance = True
        sqla_session = db.session
