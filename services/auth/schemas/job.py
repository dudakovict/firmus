from schemas import ma
from models import db, JobModel
from marshmallow import post_load
from slugify import slugify


class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobModel
        dump_only = ("slug",)
        load_only = ("category",)
        include_fk = True
        load_instance = True
        sqla_session = db.session

    @post_load
    def slugify_name(self, job, **kwargs):
        job.slug = slugify(job.name, max_length=20)
        return job
