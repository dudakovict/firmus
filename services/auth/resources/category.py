from flask import request
from flask_restful import Resource
from models.category import CategoryModel
from schemas.category import CategorySchema

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)

CATEGORY_NOT_FOUND = "Category '{}' not found."
CATEGORY_DELETED = "Category '{}' deleted."
CATEGORY_ALREADY_EXISTS = "Category '{}' already exists."
CATEGORY_ERROR_INSERTING = "An unexpected error has occured while inserting category."


class Category(Resource):
    @classmethod
    def get(cls, slug: str):
        category = CategoryModel.find_by_slug(slug)
        if category:
            return category_schema.dump(category), 200
        return {"message": CATEGORY_NOT_FOUND.format(slug)}, 404

    @classmethod
    def delete(cls, slug: str):
        category = CategoryModel.find_by_slug(slug)
        if category:
            category.delete_from_db()
            return {"message": CATEGORY_DELETED.format(slug)}, 200
        return {"message": CATEGORY_NOT_FOUND.format(slug)}, 404


class CategoryList(Resource):
    @classmethod
    def get(cls):
        return {"categories": category_list_schema.dump(CategoryModel.find_all())}, 200

    @classmethod
    def post(cls):
        category = category_schema.load(request.get_json())
        if CategoryModel.find_by_slug(category.slug):
            return {"message": CATEGORY_ALREADY_EXISTS.format(category.slug)}, 400
        try:
            category.save_to_db()
        except:
            return {"message": CATEGORY_ERROR_INSERTING}, 500
        return category_schema.dump(category), 201