import requests as rq
import json
import datetime as dt
import re

offer_url = 'https://5ka.ru/api/v2/special_offers/'
category_url = 'https://5ka.ru/api/v2/categories/'

class Catalog:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    params = {
        'records_per_page': 20,
    }

    def __init__(self, products_url, category_url):
        self.__url = products_url
        self.__cat_url = category_url
        self.__catalog = []

    def parse_by_categories(self):
        categories_page = rq.get(self.__cat_url, headers=self.headers)
        data = categories_page.json()
        now = dt.datetime.now().strftime('%d-%m-%Y')
        for i in data:
            url = self.__url
            params = {
                'records_per_page': 20,
                'categories': i['parent_group_code'],
            }
            self.__category_catalog = []
            while url:
                response = rq.get(url, headers=self.headers, params=params)
                data = response.json()
                url = data['next']
                params = {}
                self.__category_catalog.extend(data['results'])
            cat_name = i["parent_group_name"].replace('\n', '').replace('*', '-').replace('"', '').replace(',', '-').replace(' ', '-')
            with open(f'{now}_5ka_special_offers_{cat_name}.json', 'w', encoding='UTF-8') as file:
                json.dump(self.__category_catalog, file, ensure_ascii=False)

if __name__ == '__main__':
    catalog = Catalog(offer_url, category_url)
    catalog.parse_by_categories()
    print(1)