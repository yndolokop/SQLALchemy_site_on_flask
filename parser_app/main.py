import configparser as cfg
import time
import sys
from parser_app.database import db_session
from parser_app.process_request import read_requests, process_request


def main():
    # Читаем конфигурационные параметры
    config = cfg.ConfigParser()
    config.read("../web_app/hh_config.ini")
    sqlite_db = config["SQLite"]["path"]

    i_cycle: int = 0
    while True:
        # Читаем записи со статусом 0 из БД
        rows = read_requests(db_session)
        if rows:
            # Если записи найдены, то начинаем обработку
            for row_request in rows:
                print(f"\nОбработка запроса: {row_request.search_name} {row_request.region_name} начата.")
                process_request(db_session, row_request)
                print(f"\nОбработка запроса: {row_request.search_name} {row_request.region_name} завершена.")

        else:
            # Переходим в режим ожидания
            time.sleep(5)
            sys.stdout.write("\r")
            sys.stdout.write(f"Новых запросов не найдено. Цикл {i_cycle}")
        i_cycle += 1


if __name__ == "__main__":
    main()


