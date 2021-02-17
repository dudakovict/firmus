from flask import request
from flask_restful import Resource
from models.job import JobModel
from schemas.job import JobSchema

job_schema = JobSchema()
job_list_schema = JobSchema(many=True)

JOB_NOT_FOUND = "Job '{}' not found."
JOB_DELETED = "Job '{}' deleted."
JOB_ALREADY_EXISTS = "Job '{}' already exists."
JOB_ERROR_INSERTING = "An unexpected error has occured while inserting job."


class Job(Resource):
    @classmethod
    def get(cls, slug: str):
        job = JobModel.find_by_slug(slug)
        if job:
            return job_schema.dump(job), 200
        return {"message": JOB_NOT_FOUND.format(slug)}, 404

    @classmethod
    def delete(cls, slug: str):
        job = JobModel.find_by_slug(slug)
        if job:
            job.delete_from_db()
            return {"message": JOB_DELETED.format(slug)}, 200
        return {"message": JOB_NOT_FOUND.format(slug)}, 404


class JobList(Resource):
    @classmethod
    def get(cls):
        return {"jobs": job_list_schema.dump(JobModel.find_all())}, 200

    @classmethod
    def post(cls):
        job = job_schema.load(request.get_json())
        if JobModel.find_by_slug(job.slug):
            return {"message": JOB_ALREADY_EXISTS.format(job.slug)}, 400
        try:
            job.save_to_db()
        except:
            return {"message": JOB_ERROR_INSERTING}, 500
        return job_schema.dump(job), 201
