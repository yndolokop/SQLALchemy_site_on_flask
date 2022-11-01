from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser as cfg  # плагин для работы с файлом config.ini

config_db = cfg.ConfigParser()  # создаем экземпляр класса configparser для чтения с config.ini
config_db.read("../web_app/hh_config.ini")  # читаем файл config.ini
engine = create_engine(config_db["SQLite"]["path"])  # создаем движок БД, путь считываем с config.ini
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # создаем сессию SQLAlchemy
db_session = Session()
Base = declarative_base()  # указываем вид оформления классов SQLAlchemy
Base.metadata.create_all(bind=engine)  # функция создаст таблицы в БД по именам классов.