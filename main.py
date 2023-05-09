from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class FeedbackForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(message='Поле "Имя" не может быть пустым')])
    text = TextAreaField("Отзыв", validators=[DataRequired(message='Поле "Отзыв" не может быть пустым')])
    email = EmailField("Почта", validators=[Optional()])
    rating = SelectField("Оценка", choices=[5, 4, 3, 2, 1], default=5)
    submit = SubmitField("Отправить")


class NewsForm(FlaskForm):
    title = StringField("Название новости",
                        validators=[DataRequired(message='Поле "Название новости" не может быть пустым'),
                                    Length(max=200, message="Название не может быть более 100 символов")])
    text = TextAreaField("Текст новости",
                         validators=[DataRequired(message='Поле "Текст новости" не может быть пустым')])
    category = SelectField("Категория")
    submit = SubmitField("Добавить")


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)


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


with app.app_context():
    db.create_all()


def index():
    content = News.query.all()
    categories = Category.query.all()

    return render_template("index.html", content=content, categories=categories)


def feedback():
    form = FeedbackForm()
    categories = Category.query.all()

    if form.validate_on_submit():
        feedback_model = Feedback()

        feedback_model.name = form.name.data
        feedback_model.text = form.text.data
        feedback_model.email = form.email.data
        feedback_model.rating = form.rating.data

        db.session.add(feedback_model)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("feedback.html", form=form, categories=categories)


def add_news():
    form = NewsForm()
    categories = Category.query.all()
    form.category.choices = [cat.title for cat in categories]

    if form.validate_on_submit():
        news_model = News()

        news_model.title = form.title.data
        news_model.text = form.text.data
        news_model.category_id = Category.query.filter(Category.title == form.category.data).first().id

        db.session.add(news_model)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_news.html", form=form, categories=categories)


def news_detail(id):
    content = News.query.get(id)
    categories = Category.query.all()

    return render_template("news_detail.html", news=content, categories=categories)


def category(id):
    category_object = Category.query.get(id)
    content = category_object.news
    category_name = category_object.title
    categories = Category.query.all()

    return render_template("categories.html", category_name=category_name, content=content, categories=categories)


app.add_url_rule('/', view_func=index)
app.add_url_rule('/feedback', 'feedback', feedback, methods=["GET", "POST"])
app.add_url_rule('/add_news', 'add_news', add_news, methods=["GET", "POST"])
app.add_url_rule('/news_detail/<int:id>', 'news_detail', news_detail)
app.add_url_rule('/category/<string:id>', 'category', category)


# if __name__ == "__main__":
#     app.run(debug=True)
