from flask import Blueprint, render_template, request, session, redirect, flash, url_for
from sqlalchemy import desc
import parser_app.get_IDs_by_name as id
import parser_app.hhrequest as hh
from flask_table import Table, Col, LinkCol
from datetime import datetime
from web_app.models import Request
from web_app.database import db_session




LT = [{'id': '0', 'name': 'везде'},
     {'id': '1', 'name': 'Информационные технологии, интернет, телеком'},
     {'id': '2', 'name': 'Бухгалтерия, управленческий учет, финансы предприятия'},
     {'id': '3', 'name': 'Маркетинг, реклама, PR'},
     {'id': '4', 'name': 'Административный персонал'},
     {'id': '5', 'name': 'Банки, инвестиции, лизинг'},
     {'id': '6', 'name': 'Управление персоналом, тренинги'},
     {'id': '7', 'name': 'Автомобильный бизнес'},
     {'id': '8', 'name': 'Безопасность'},
     {'id': '9', 'name': 'Высший менеджмент'},
     {'id': '10', 'name': 'Добыча сырья'},
     {'id': '11', 'name': 'Искусство, развлечения, масс-медиа'},
     {'id': '12', 'name': 'Консультирование'},
     {'id': '13', 'name': 'Медицина, фармацевтика'},
     {'id': '14', 'name': 'Наука, образование'},
     {'id': '15', 'name': 'Начало карьеры, студенты'},
     {'id': '16', 'name': 'Государственная служба, некоммерческие организации'},
     {'id': '17', 'name': 'Продажи'},
     {'id': '18', 'name': 'Производство, сельское хозяйство'},
     {'id': '19', 'name': 'Страхование'},
     {'id': '20', 'name': 'Строительство, недвижимость'},
     {'id': '21', 'name': 'Транспорт, логистика'},
     {'id': '22', 'name': 'Туризм, гостиницы, рестораны'},
     {'id': '23', 'name': 'Юристы'},
     {'id': '24', 'name': 'Спортивные клубы, фитнес, салоны красоты'},
     {'id': '25', 'name': 'Инсталляция и сервис'},
     {'id': '26', 'name': 'Закупки'},
     {'id': '27', 'name': 'Домашний персонал'},
     {'id': '29', 'name': 'Рабочий персонал'}]


parser_blueprint = Blueprint("flask_parser", __name__)

find_id = id.ID()
parser = hh.Parser()

# Создание таблицы для вывода на странице История
class ItemTable(Table):
    # Атрибуты таблицы, которые будут использованы при ввыоде ее на экран
    classes = ["table", "table-bordered"]
    tab_id = Col("Номер запроса")
    region_name = Col('Регион')
    search_name = Col('Запрос')
    count = Col("Кол-во от всех вакансий")
    percent = Col("% от всех вакансий")
    status = Col("Статус")
    created = Col("Создан")
    name = LinkCol('Смотреть', 'flask_parser.single_item',
                   url_kwargs=dict(id='tab_id'))


@parser_blueprint.route("/")
def root():
    """
       Функция обработки запроса к корневой странице
    :return Страница Index
    """
    return render_template("index.html")


@parser_blueprint.route("/index/")
def index():
    """
       Функция обработки запроса к странице Index
    :return Страница Index
    """
    return render_template("index.html")


@parser_blueprint.route("/run/", methods=["GET"])
def run_get():
    drop_list = find_id.get_specialization_list()
    if not drop_list:
        drop_list = LT
    return render_template('form.html', drop_list=drop_list)


@parser_blueprint.route("/post/", methods=["GET", "POST"])  # соединяет с базой, запрашивает таблицу в базе и рендерит ее на страницу
def show_parsing_result():
    drop_list = find_id.get_specialization_list()
    rows = db_session.query(Request).filter(Request.status == 2).order_by(desc(Request.created)).first()
    if rows:
        data = rows.data
        return render_template('form.html', data=data,  drop_list=drop_list)


@parser_blueprint.route("/run/", methods=["GET", "POST"])
def requests():
    """
        Функция обработки запроса к странице 'Запросы'
        :return: Обработанную страницу 'Запросы'
    """
    # Эта страница доступна только авторизованному пользователю
    if session.get("user_id"):
        # key_count = parser.total_vacancy(row_request.search_name, result)
        # Обработка формы по запросу
        if request.method == "POST":

            # Достаем нужные данные из формы запроса
            field = request.form['search_by_field']
            region = request.form['region']
            search_name = request.form['search_by']  # достаем из формы в form.html из параметра name текст запроса
            try:
                # Проверяем правильность задания региона
                region = find_id.check_region_name(region)
            except ValueError as ex:
                flash("Регион указан не правильно " + str(ex))
                return render_template("form.html")
            # Берем регион из проверки.
            # Вставляем запрос в БД для обработки
            request_db = Request(user_id=session["user_id"],
                                 field_name=field,
                                 region_name=region,
                                 search_name=search_name,
                                 status=0,
                                 created=datetime.now())
            db_session.add(request_db)
            db_session.commit()
            flash("Запрос отправлен на обработку. Ждите...", category='success')

    else:
        # Если пользователь не авторизован, то отправляем его в Login
        return redirect(url_for('auth.login'))
    button = 'Посмотреть результат'
    return render_template("form.html", title='Запросы', button=button)


@parser_blueprint.route("/contacts/", methods=["GET", "POST"])
def contacts():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contacts.html', title='Контакты')