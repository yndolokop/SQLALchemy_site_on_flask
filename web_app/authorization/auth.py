from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from .forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from web_app.database import db_session
from web_app.models import User
from datetime import datetime

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form['username']
        email = request.form["email"]
        password = request.form["psw"]
        repeat_password = request.form["psw2"]
        row = db_session.query(User).filter(User.email == email).all()
        if not row:
            # Проверяем пароль
            if len(request.form['username']) > 2 \
                    and len(request.form['email']) > 2 \
                    and len(request.form['psw']) > 4 \
                    and password == repeat_password:
                flash("Вы успешно зарегистрированы", category="success")
                h_password = generate_password_hash(password)
                user = User(name, email, datetime.now(), h_password)
                db_session.add(user)
                db_session.commit()
                # Отправляем пользователя на страницу авторизации
                return redirect(url_for('auth.login'))

            else:
                flash("Неправильно заполнены поля.", category="error")
        else:
            flash("Такой пользователь уже cуществует. Используйте другой адрес электронной почты.", category="error")
            return redirect(url_for('auth.register'))
    return render_template('register.html', title='Регистрация')


@auth_blueprint.route("/login/", methods=["POST", "GET"])  # обработчик авторизации пользователя
def login():
    form = LoginForm()
    if request.method == "POST":
        email = form.email.data
        password = form.psw.data
        row = db_session.query(User).filter(User.email == email).all()
        if not row:
            flash("Такой пользователь не зарегистрирован.", category="error")
        else:
            user_id = row[0].id
            user_name = row[0].name
            h_password = row[0].password
            if check_password_hash(h_password, password):
                session["user_name"] = user_name
                session["user_id"] = user_id
                return redirect(url_for('flask_parser.index'))
            else:
                # Если пароль не правильный, то выдаем сообщение об ошибке
                flash("Указан неверный пароль")

    return render_template('login_flask_forms.html', title='Авторизация', form=form)


@auth_blueprint.route("/logout/", methods=["POST", "GET"])
def logout():
    """
        Функция завершения сессии работы
    :return:
    """
    form = LoginForm()
    if request.method == "POST":
        flash("Подтвердите выход")
        # Удаляем из сессии атрибуты пользователя
        del session["user_id"]
        del session["user_name"]
        return redirect(url_for('auth.login'))
    return render_template("logout.html", title='Логаут', form=form)


# @auth_blueprint.route("/forgot-password", methods=["GET", "POST"])
# def forgot_password():
#     return render_template("forgot-password.html")