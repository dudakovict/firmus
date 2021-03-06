from flask import request
from flask_restful import Resource
from models import JobModel, CategoryModel
from schemas import JobSchema
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError
from errors import (
    JobAlreadyExistsError,
    JobNotExistsError,
    JobForeignKeyError,
    InternalServerError,
)

job_schema = JobSchema()
job_list_schema = JobSchema(many=True)


class Job(Resource):
    @classmethod
    def get(cls, slug: str):
        job = JobModel.find_by_slug(slug)
        if job is None:
            raise JobNotExistsError
        return job_schema.dump(job), 200

    @classmethod
    def delete(cls, slug: str):
        job = JobModel.find_by_slug(slug)
        if job is None:
            raise JobNotExistsError
        job.delete_from_db()
        return None, 204


class JobList(Resource):
    @classmethod
    def get(cls):
        return {"jobs": job_list_schema.dump(JobModel.find_all())}, 200

    @classmethod
    def post(cls):
        job = job_schema.load(request.get_json())
        try:
            if CategoryModel.find_by_slug(job.category_slug) is None:
                raise ForeignKeyViolation
            job.save_to_db()
        except ForeignKeyViolation:
            raise JobForeignKeyError
        except IntegrityError:
            raise JobAlreadyExistsError
        except:
            raise InternalServerError
        return job_schema.dump(job), 201
