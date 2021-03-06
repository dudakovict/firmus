from models import db
from typing import List


class CategoryModel(db.Model):
    __tablename__ = "categories"

    slug = db.Column(db.String(20), unique=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    jobs = db.relationship("JobModel", lazy="dynamic")

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_slug(cls, slug: str) -> "CategoryModel":
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_all(cls) -> List["CategoryModel"]:
        return cls.query.all()
