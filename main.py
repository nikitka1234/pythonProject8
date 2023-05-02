from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional


class FeedbackForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(message='Поле "Имя" не может быть пустым')])
    text = TextAreaField("Отзыв", validators=[DataRequired(message='Поле "Отзыв" не может быть пустым')])
    email = EmailField("Почта", validators=[Optional()])
    rating = SelectField("Оценка", choices=[5, 4, 3, 2, 1], default=5)
    submit = SubmitField("Отправить")


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

content = [
    {"title": "Название для шаблона из словаря", "text": "Текст для шаблона из словаря"},
    {"title": "Экс-глава регионального СК назначен главным федеральным инспектором", "text": "Бывший руководитель следственного управления Следственного комитета по Свердловской области Михаил Богинский назначен главным федеральным инспектором региона. Как сообщили в пресс-службе полпредства, соответствующее распоряжение подписал полномочный представитель президента в УрФО Владимир Якушев."},
    {"title": "Посол Швейцарии выступил в защиту отказа от передачи Украине боеприпасов", "text": "Посол Швейцарии в Берлине Пауль Зегер выступил в защиту решения правительства страны об отказе передавать Украине боеприпасы швейцарского производства. О своей позиции он заявил изданию Augsburger Allgemeine."}
]
news_list = [
    {"title": 734764, "text": "text for 734764"},
    {"title": 734764, "text": "text for 734764"},
    {"title": 734764, "text": "text for 734764"}
]


def index():
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


def news_detail(id):
    return render_template("news_detail.html", **content[id])


def category(name):
    return f"Категория {name}"


app.add_url_rule('/', view_func=index)
app.add_url_rule('/feedback', 'feedback', feedback, methods=["GET", "POST"])
app.add_url_rule('/news_detail/<int:id>', 'news_detail', news_detail)
app.add_url_rule('/category/<string:name>', 'category', category)


# if __name__ == "__main__":
#     app.run(debug=True)
