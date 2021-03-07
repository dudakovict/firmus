from models import db, user_jobs
from typing import List


class JobModel(db.Model):
    __tablename__ = "jobs"

    slug = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category_slug = db.Column(
        db.String(20), db.ForeignKey("categories.slug"), nullable=False
    )
    category = db.relationship("CategoryModel")
    users = db.relationship(
        "UserModel", secondary=user_jobs, lazy="dynamic", back_populates="jobs"
    )

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
