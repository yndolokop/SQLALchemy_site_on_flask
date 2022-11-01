import requests


class ID:
    def __init__(self):

        self.area_list = []
        self.field_id = int
        self.region_id = int
        self.region_text = ""
        self.field_list = []

    def get_specialization_list(self):
        area_result = requests.get('https://api.hh.ru/specializations').json()  # страница со списком сфер деятельности.
        c = []  # Список для хранения названий сфер деятельности и специальностей. Например, Бухгалтерия или Маркетинг
        b = {'id': '0', 'name': 'искать везде'}  # Элемент поиска 'везде', добавим в список с. Парсер будет искать
        # везде, если
        # id специализации будет 0.

        for i in area_result:
            c.append(dict(id=i['id'], name=i['name']))
        c.append(b)
        self.field_list = sorted(c, key=lambda x: int(x['id']))
        return self.field_list

    def get_specialization_id(self, field_name):
        """Формирует список из словарей областей деятельности, который будем подавать в выпадающий
        список меню на странице поиска"""

        area_result = requests.get(
            'https://api.hh.ru/specializations').json()  # адресс со списком областей деятельности.
        c = []  # Список для хранения названий сфер деятельности и специальностей. Например, Бухгалтерия или Маркетинг
        b = {'id': '0', 'name': 'везде'}  # элемент поиска 'везде', который добавим в список с.

        for i in area_result:
            a = dict(id=i['id'], name=i['name'])  # из добавим словари в список c.
            c.append(a)
        c.append(b)
        self.area_list = sorted(c, key=lambda x: int(x['id']))  # упорядоченый по ключу ['id'} словарь

        for i in self.area_list:
            if i['name'] == field_name:
                self.field_id = i['id']
                return self.field_id  # возвращает id области деятельности

    def get_region_id(self, region_name):  # принимает регион, проверяет его на правильность и возвращает id региона
        params = {'text': region_name}
        region_result = requests.get('https://api.hh.ru/suggests/areas', params=params).json()  # регионы
        if region_result["items"]:
            self.region_id = region_result["items"][0]["id"]
        else:
            raise ValueError("Регион не найден.")
        return self.region_id

    def check_region_name(self, region_name):  # проверяет введеный пользователем регион в списке регионов из api
        params = {'text': region_name}
        region_result = requests.get('https://api.hh.ru/suggests/areas', params=params).json()  # регионы
        if region_result["items"]:

            self.region_text = region_result["items"][0]["text"]
        else:
            raise ValueError("Регион не найден.")
        return self.region_text  # возвращает текст, если регион найден


# if __name__ == '__main__':
#     pass
