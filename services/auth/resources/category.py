from flask import request
from flask_restful import Resource
from models import CategoryModel
from schemas import CategorySchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from errors import (
    CategoryAlreadyExistsError,
    CategoryNotExistsError,
    CategoryNotNullError,
    InternalServerError,
)

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


class Category(Resource):
    @classmethod
    def get(cls, slug: str):
        category = CategoryModel.find_by_slug(slug)
        if category is None:
            raise CategoryNotExistsError
        return category_schema.dump(category), 200

    @classmethod
    def delete(cls, slug: str):
        category = CategoryModel.find_by_slug(slug)
        try:
            if category is None:
                raise NoResultFound
            category.delete_from_db()
        except NoResultFound:
            raise CategoryNotExistsError
        except IntegrityError:
            raise CategoryNotNullError
        except:
            raise InternalServerError
        return None, 204


class CategoryList(Resource):
    @classmethod
    def get(cls):
        return {"categories": category_list_schema.dump(CategoryModel.find_all())}, 200

    @classmethod
    def post(cls):
        category = category_schema.load(request.get_json())
        try:
            category.save_to_db()
        except IntegrityError:
            raise CategoryAlreadyExistsError
        except:
            raise InternalServerError
        return category_schema.dump(category), 201
