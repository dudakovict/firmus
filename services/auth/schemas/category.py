from schemas import ma, JobSchema
from models import db, CategoryModel, JobModel
from marshmallow import post_load
from slugify import slugify


class CategorySchema(ma.SQLAlchemyAutoSchema):
    jobs = ma.Nested(JobSchema, many=True)

    class Meta:
        model = CategoryModel
        dump_only = ("slug",)
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @post_load
    def slugify_name(self, category, **kwargs):
        category.slug = slugify(category.name, max_length=20)
        return category
