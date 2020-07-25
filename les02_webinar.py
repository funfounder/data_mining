from bs4 import BeautifulSoup as bs
import requests
import lxml
import json

class GbBlogParse:
    __domain = 'https://geekbrains.ru'
    __url = 'https://geekbrains.ru/posts'
    __done_urls = set()

    def __init__(self):
        self.posts_urls = set()
        self.pagination_urls = set()
        self.posts_lib = dict()

    def get_page_soap(self, url):
        # todo метод запроса страницы и создания супа
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        return soup

    def run(self, url=None):
        # todo метод запуска парсинга
        url = url or self.__url
        soup = self.get_page_soap(url)
        self.pagination_urls.update(self.get_pagination(soup))
        self.posts_urls.update(self.get_posts_urls(soup))
        self.posts_lib.update(self.get_posts_data())

        for url in tuple(self.pagination_urls):
            if url not in self.__done_urls:
                self.__done_urls.add(url)
                self.run(url)

    def get_posts_data(self):
        posts_url = tuple(self.posts_urls)
        posts_lib = []
        for i in posts_url:
            post_data = {}
            response = requests.get(i)
            soup = bs(response.text, 'lxml')
            author_block = soup.find('div', attrs={'class': 'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'})
            article_block = soup.find('article')
            post_data['title'] = soup.find('h1', attrs={'class': 'blogpost-title'}).get_text()
            post_data['post_url'] = i
            post_data['writer_name'] = soup.find('div', attrs={'itemprop': 'author'}).get_text()
            post_data['writer_url'] = f'{self.__domain}{author_block.find("a").get("href")}'
            tags = []
            for itm in article_block.find_all("a", attrs={"class": "small"}):
                tags.append({itm.get_text():f'{self.__domain}{itm.get("href")}'})
            post_data['tags'] = tags
            posts_lib.append(post_data)
        return posts_lib

    def save_to_file(self):
        with open('posts_lib.json', 'w', encoding='UTF-8') as file:
            json.dump(self.post_lib, file, ensure_ascii=False)

    # todo Проход пагинации ленты
    def get_pagination(self, soup):
        ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        a_list = [f'{self.__domain}{a.get("href")}' for a in ul.find_all('a') if a.get("href")]
        return a_list

    # todo Поиск ссылок на статьи на странице ленты
    def get_posts_urls(self, soup):
        posts_wrap = soup.find('div', attrs={'class': 'post-items-wrapper'})
        a_list = [f'{self.__domain}{a.get("href")}' for a in
                  posts_wrap.find_all('a', attrs={'class': 'post-item__title'})]
        return a_list


if __name__ == '__main__':
    parser = GbBlogParse()
    parser.run()
    parser.get_posts_data()
    parser.save_to_file()
    print(1)