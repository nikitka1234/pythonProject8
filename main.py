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
    submit = SubmitField("Добавить")


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())


with app.app_context():
    db.create_all()


def index():
    content = News.query.all()

    return render_template("index.html", content=content)


def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        email = form.email.data
        rating = form.rating.data

        print(name, text, email, rating, sep="\n\n---------------------\n\n")

        return redirect(url_for("index"))

    return render_template("feedback.html", form=form)


def add_news():
    form = NewsForm()

    if form.validate_on_submit():
        news_model = News()

        news_model.title = form.title.data
        news_model.text = form.text.data

        db.session.add(news_model)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_news.html", form=form)


def news_detail(id):
    content = News.query.get(id)

    return render_template("news_detail.html", news=content)


def category(name):
    return f"Категория {name}"


app.add_url_rule('/', view_func=index)
app.add_url_rule('/feedback', 'feedback', feedback, methods=["GET", "POST"])
app.add_url_rule('/add_news', 'add_news', add_news, methods=["GET", "POST"])
app.add_url_rule('/news_detail/<int:id>', 'news_detail', news_detail)
app.add_url_rule('/category/<string:name>', 'category', category)


# if __name__ == "__main__":
#     app.run(debug=True)
