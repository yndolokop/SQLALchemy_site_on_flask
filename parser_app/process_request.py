from sqlalchemy import desc
from datetime import datetime
from web_app.models import Request
import parser_app.get_IDs_by_name as id
import parser_app.hhrequest as hh


def process_request(db_path, row_request):
    '''
        Функция обработки запроса, прочитанного из БД
    :param db_path: путь к БД
    :param file_folder: путь к файлам с результатами
    :param row_request: запрос, прочитанный из БД
    '''

    # Меняем статус на "В обработке"
    update_status(db_path, row_request, 1)
    # Задаем начальные значения поиска
    url = 'https://api.hh.ru/vacancies?'
    find_id = id.ID()
    parser = hh.Parser()
    region_id = find_id.get_region_id(row_request.region_name)
    specialization_id = find_id.get_specialization_id(row_request.field_name)
    params = parser.get_params_no_desc(row_request.search_name, region_id, specialization_id)
    result = parser.get_json_from_api(url, params)
    key_count = parser.total_vacancy(row_request.search_name, result)
    data = parser.skills_search(url, result, row_request.search_name, region_id, specialization_id)
    # Обновляем запись с результатами запроса
    update_request(db_path, row_request, data)


def read_requests(db_session):
    """
         Функция чтения запросов из БД
    :param db_session: сессия БД
    :return: список найденных записей
    """
    # Выбираем все запросы из БД со статусом 0
    row = db_session.query(Request).filter(Request.status == 0).order_by(desc(Request.created)).all()
    return row


def update_request(db_session, row_request, data):
    """
        Функция обновления записи запроса в БД
    :param row_request: запись, которую надо обновить
    :param db_session: сессия БД
    :param file_name: имя файла с результатами
    """
    # Формируем запрос к БД
    db_session.query(Request).filter(Request.id == row_request.id). \
        update({Request.data: data, Request.status: 2})
    db_session.commit()


def update_status(db_session, row_request, status):
    """
        Функция изменеия статуса запроса в БД
    :param row_request: запись, статус в которой надо обновить
    :param db_session: сессия БД
    :param status: статус
    """
    # Если статус меняется на один (В обработке), то не надо изменять кол-во вакансий
    if status == 1:
        db_session.query(Request).filter(Request.id == row_request.id). \
            update({Request.status: status, Request.updated: datetime.now()},
                   synchronize_session=False)
        db_session.commit()
    else:
        db_session.query(Request).filter(Request.id == row_request.id). \
            update({Request.status: status, Request.created: datetime.now()},
                   synchronize_session=False)
        db_session.commit()
