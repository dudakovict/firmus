from db import db
from slugify import slugify
from typing import List


class JobModel(db.Model):
    __tablename__ = "jobs"

    slug = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category_slug = db.Column(
        db.String(20), db.ForeignKey("categories.slug"), nullable=False
    )
    category = db.relationship("CategoryModel")

    def __init__(self, name: str, category_slug: str, **kwargs):
        super().__init__(**kwargs)
        self.slug = slugify(name, max_length=20)
        self.name = name
        self.category_slug = category_slug

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_slug(cls, slug: str) -> "JobModel":
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_all(cls) -> List["JobModel"]:
        return cls.query.all()
