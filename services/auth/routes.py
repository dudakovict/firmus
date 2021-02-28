from resources.category import CategoryList, Category
from resources.job import JobList, Job
from resources.auth import (
    UserRegister,
    UserCheckVerification,
    UserResendVerification,
    UserLogin,
)


def initialize_routes(api):
    api.add_resource(CategoryList, "/categories", endpoint="categories")
    api.add_resource(Category, "/categories/<string:slug>", endpoint="category")

    api.add_resource(JobList, "/jobs", endpoint="jobs")
    api.add_resource(Job, "/jobs/<string:slug>", endpoint="job")

    api.add_resource(UserRegister, "/auth/register", endpoint="register")
    api.add_resource(UserCheckVerification, "/auth/verify", endpoint="verify")
    api.add_resource(UserResendVerification, "/auth/resend", endpoint="resend")
    api.add_resource(UserLogin, "/auth/login", endpoint="login")
