from werkzeug.exceptions import HTTPException

#####################
# Category Exceptions
#####################


class CategoryAlreadyExistsError(HTTPException):
    pass


class CategoryNotExistsError(HTTPException):
    pass


class CategoryNotNullError(HTTPException):
    pass


#####################
# Job Exceptions
#####################


class JobAlreadyExistsError(HTTPException):
    pass


class JobNotExistsError(HTTPException):
    pass


class JobForeignKeyError(HTTPException):
    pass


#####################
# User Exceptions
#####################


class UserEmailAlreadyExistsError(HTTPException):
    pass


class UserPhoneAlreadyExistsError(HTTPException):
    pass


class UserPhoneNotExistsError(HTTPException):
    pass


class UserEmailNotExistsError(HTTPException):
    pass


class UserNotVerifiedError(HTTPException):
    pass


class UserAlreadyVerifiedError(HTTPException):
    pass


#####################
# General Exceptions
#####################


class InvalidCredentialsError(HTTPException):
    pass


class InvalidPhoneNumberError(HTTPException):
    pass


class InvalidVerificationCodeError(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


errors = {
    "InternalServerError": {"message": "Something went wrong.", "status": 500},
    "CategoryAlreadyExistsError": {
        "message": "Category with that name already exists.",
        "status": 400,
    },
    "CategoryNotExistsError": {
        "message": "Category with that name doesn't exist.",
        "status": 404,
    },
    "CategoryNotNullError": {
        "message": "Violation of not-null constraint.",
        "status": 400,
    },
    "JobAlreadyExistsError": {
        "message": "Job with that name already exists.",
        "status": 400,
    },
    "JobNotExistsError": {"message": "Job with that name doesn't exist", "status": 404},
    "JobForeignKeyError": {
        "message": "Foreign key constraint violation. No such category.",
        "status": 400,
    },
    "UserEmailAlreadyExistsError": {
        "message": "User with that email already exists.",
        "status": 400,
    },
    "UserPhoneAlreadyExistsError": {
        "message": "User with that phone number already exists.",
        "status": 400,
    },
    "UserPhoneNotExistsError": {
        "message": "User with that phone number doesn't exist.",
        "status": 404,
    },
    "UserEmailNotExistsError": {
        "message": "User with that email doesn't exist.",
        "status": 404,
    },
    "UserNotVerifiedError": {"message": "User has not been verified.", "status": 400},
    "UserAlreadyVerifiedError": {
        "message": "User has already been verified.",
        "status": 400,
    },
    "InvalidPhoneNumberError": {
        "message": "Invalid phone number. Please provide the phone number in E164 format: [+] [country code] [subscriber number including area code].",
        "status": 400,
    },
    "InvalidVerificationCodeError": {
        "message": "Invalid verification code.",
        "status": 400,
    },
    "InvalidCredentialsError": {"message": "Invalid credentials.", "status": 401},
}
