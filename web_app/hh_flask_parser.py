from parser_app import main as pr
import multiprocessing as ml
from web_app import create_app

if __name__ == "__main__":
    # Создать приложение Flask
    app = create_app()

    # Запустить парсер через мультипроцесс
    par_service = ml.Process(name="HH API Parser", target=pr.main)
    par_service.start()

    # Запустить Flask приложение
    app.run()