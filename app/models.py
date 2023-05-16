from . import db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    news = db.relationship("News", back_populates="category")

    def __repr__(self):
        return f"Category: {self.title}"


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category", back_populates="news")

    def __repr__(self):
        return f"News: {self.title}, {self.text[:15]}"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    text = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Integer, nullable=False, default=5)
    date = db.Column(db.DateTime, default=datetime.utcnow())
