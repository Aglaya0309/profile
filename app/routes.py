from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@main_routes.route('/home')
def home():
    return render_template('home.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Введённые данные неверны.', 'danger')
    return render_template('login.html', form=form)

@main_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main_routes.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Меняем имя пользователя и эл.почту
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Проверяем, установлен ли новый пароль
        if form.new_password.data:
            # Генерируем новый хэшированный пароль
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password

        db.session.commit()
        flash('Ваш аккаунт был успешно обновлён!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form)