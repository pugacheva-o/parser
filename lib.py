import requests
import re
from bs4 import BeautifulSoup
import pandas
from lxml import etree as et

# получаем html страницы
def get_page_content(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req.text

# получаем номер GTM
def extract_gtm(page_content):
    match = re.search(r'GTM-[0-9a-zA-Z]+', page_content)
    if match is not None:
        return match.group(0)
    return "GTM не найден"

# получаем номер яндекс метрики
def extract_ym(page_content):
    match = re.search(r'ym\([0-9]+,', page_content)
    if match is not None:
        ym = re.search(r'[0-9]+', match.group(0))
        return ym.group(0)

    return "YM не найден"

# получаем ссылки на странице по условиям (на выходе множество)
def get_links_on_page(page_content, domain):
    all_pages = set()
    # тут список страниц для обхода
    uniq_page = set()
    soup = BeautifulSoup(page_content, 'html.parser')
    # цикл и условия добавления страниц в список uniq_page
    for link in soup.find_all('a'):
        if len(uniq_page) < 5:
            url = link.get('href')
            if url:
                url = url.split('#')[0]
            if url:
                if domain in url:
                    url = url.replace(domain, '')
            if url.startswith('http') or url.startswith('mail') or url.startswith('tel'):
                continue
            uniq_page.add(url)
        else:
            break
    return uniq_page

'''
попытка сделать функцию, которая будет получать все ссылки сайта
def get_all_pages():
    all_pages = set() # Множество урлов сайта
    if len(all_pages) < 15:
        nexturl = get_links_on_page() # следующий урл получает
        all_pages.add(nexturl)
    return all_pages
'''

