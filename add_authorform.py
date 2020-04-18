from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class Add_authorForm(FlaskForm):
    name = StringField('Имя и Фамилия автора', validators=[DataRequired()])
    submit = SubmitField('Добавить')
