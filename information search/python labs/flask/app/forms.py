from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Войти")

class RegistrationForm(LoginForm):
    password_repeat = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password", message="Пароли должны совпадать.")],
    )
    submit = SubmitField("Зарегистрироваться")

class UniversityForm(FlaskForm):
    full_name = StringField(
        "Полное название", validators=[DataRequired(), Length(min=2, max=255)]
    )
    short_name = StringField(
        "Сокращенное название", validators=[DataRequired(), Length(min=1, max=50)]
    )
    foundation_date = DateField(
        "Дата создания", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("Сохранить")

    def validate_foundation_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError("Дата создания не может быть в будущем.")

class StudentForm(FlaskForm):
    full_name = StringField("ФИО", validators=[DataRequired(), Length(min=2, max=255)])
    birth_date = DateField(
        "Дата рождения", format="%Y-%m-%d", validators=[DataRequired()]
    )
    university_id = SelectField("Университет", coerce=int, validators=[DataRequired()])
    admission_year = IntegerField(
        "Год поступления",
        validators=[DataRequired(), NumberRange(min=1900, max=date.today().year + 1)],
    )
    submit = SubmitField("Сохранить")

    def validate_birth_date(self, field):
        if field.data and field.data > date.today():
            raise ValidationError("Дата рождения не может быть в будущем.")
