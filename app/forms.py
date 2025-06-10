from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User
from app import bcrypt  # для проверки старых паролей


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('Эл. почта', validators=[InputRequired(), Email()])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Такой пользователь уже существует.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Данный почтовый ящик занят.')


class LoginForm(FlaskForm):
    email = StringField('Эл. почта', validators=[InputRequired(), Email()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('Эл. почта', validators=[InputRequired(), Email()])
    old_password = PasswordField('Старый пароль', validators=[InputRequired()])  # новое поле
    new_password = PasswordField('Новый пароль', validators=[Length(min=6)])  # новое поле
    confirm_password = PasswordField('Подтвердите новый пароль', validators=[EqualTo('new_password')])  # новое поле
    submit = SubmitField('Обновить профиль')

    def validate_old_password(self, field):
        # проверка правильности старого пароля
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Старый пароль неверен.')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Такое имя пользователя уже занято.')

    def validate_email(self, field):
        if field.data != current_user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Такая почта уже используется.')