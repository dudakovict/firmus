from resources import (
    CategoryList,
    Category,
    JobList,
    Job,
    UserRegister,
    UserCheckVerification,
    UserResendVerification,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh,
    TokenRefresh,
)


def initialize_routes(api):
    api.add_resource(CategoryList, "/categories", endpoint="categories")
    api.add_resource(Category, "/categories/<string:slug>", endpoint="category")

    api.add_resource(JobList, "/jobs", endpoint="jobs")
    api.add_resource(Job, "/jobs/<string:slug>", endpoint="job")

    api.add_resource(UserRegister, "/register", endpoint="register")
    api.add_resource(UserCheckVerification, "/verify", endpoint="verify")
    api.add_resource(UserResendVerification, "/resend", endpoint="resend")
    api.add_resource(UserLogin, "/login", endpoint="login")
    api.add_resource(UserLogoutAccess, "/logout/access", endpoint="logout/access")
    api.add_resource(UserLogoutRefresh, "/logout/refresh", endpoint="logout/refresh")
    api.add_resource(TokenRefresh, "/token/refresh", endpoint="token/refresh")
