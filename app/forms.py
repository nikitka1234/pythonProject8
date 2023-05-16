from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


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
