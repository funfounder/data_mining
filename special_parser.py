import json
import datetime as dt
import requests


class Catalog:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    }
    params = {
        'records_per_page': 50,
    }

    def __init__(self, url):
        self.__url = url
        self.__catalog = []

    def parse(self):
        url = self.__url
        params = self.params

        while url:
            response = requests.get(url, headers=self.headers, params=params)
            data = response.json()
            url = data['next']
            params = {}
            self.__catalog.extend(data['results'])

    def save_to_file(self):
        now = dt.datetime.now().strftime('%d-%m-%Y')
        with open(f'{now}_5kacatalog.json', 'w', encoding='UTF-8') as file:
            json.dump(self.__catalog, file, ensure_ascii=False)


if __name__ == '__main__':
    catalog = Catalog('https://5ka.ru/api/v2/special_offers/')
    catalog.parse()
    print(1)