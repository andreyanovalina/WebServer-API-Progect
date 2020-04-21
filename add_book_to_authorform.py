from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class Add_book_to_authorForm(FlaskForm):
    name = StringField('Имя и фамилия автора', validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = TextAreaField('Цена(р.)', validators=[DataRequired()])
    submit = SubmitField('Добавить')
