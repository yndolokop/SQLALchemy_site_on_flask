import requests


class Parser:
    def __init__(self):
        self.params_no_desc = {}
        self.params_with_desc = {}
        self.total_vacancies = {}
        self.skills = {}

    def get_params_no_desc(self, search_name, region_id, specialization_id=0):
        if specialization_id == 0:
            self.params_no_desc = {'text': f"NAME:({search_name})", 'area': f"{region_id}"}
        else:
            self.params_no_desc = {'text': f"NAME:({search_name})", 'area': f"{region_id}",
                                   'specialization': f"{specialization_id}"}
        return self.params_no_desc

    def get_params_with_desc(self, search_name, i, region_id, specialization_id=0):
        if specialization_id == 0:
            self.params_with_desc = {'text': f"NAME:({search_name}) AND DESCRIPTION:({i})", 'area': f"{region_id}"}
        else:
            self.params_with_desc = {'text': f"NAME:({search_name}) AND DESCRIPTION:({i})",
                                     'area': f"{region_id}",
                                     'specialization': f"{specialization_id}"}
        return self.params_with_desc

    @staticmethod
    def get_json_from_api(url, params):
        return requests.get(url, params=params).json()

    def total_vacancy(self, search_name, result):
        self.total_vacancies = dict(keyword=search_name, count=result['found'])
        return self.total_vacancies

    def list_of_skills_from_description(self, result):
        a = []
        items = result['items']
        for element in items:
            url_ = element['url']  # берем из items ccылку на вакансию, проходим и достаем оттуда по ключу навыки.
            result = requests.get(url_).json()
            for p in result['key_skills']:  # по этому ключу достаем навыки.
                a.append(p['name'])
                self.skills = set(a)
        return self.skills

    def skills_search(self, url, result, search_name, region_id, specialization_id):
        final_list_of_counts = []
        for i in self.list_of_skills_from_description(result):
            params = self.get_params_with_desc(search_name, i, region_id, specialization_id)
            result_vacancies = self.get_json_from_api(url, params)
            num_of_one_skill = result_vacancies['found']
            a = dict(name=i, count=num_of_one_skill,
                     percent='{0:.1f}'.format(100 * num_of_one_skill / self.total_vacancies['count']))
            final_list_of_counts.append(a)
            final_list_of_counts = sorted(final_list_of_counts, key=lambda x: x['count'], reverse=True)
        return final_list_of_counts
