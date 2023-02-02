import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json


url_list = []
url_narm_jab_list = []
fin_list = []
HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def h():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()


def _vacancy_url():
    resource = requests.get(HOST, headers=h())
    resource_text = resource.text
    soup = BeautifulSoup(resource_text, features='lxml')
    vacancy_list = soup.find('div', class_='vacancy-serp-content')
    vacancy = vacancy_list.find_all('div', class_='vacancy-serp-item__layout')
    for i in vacancy:
        tag = i.find('a')
        url = tag['href']
        url_list.append(url)


def _brand_user():
    _vacancy_url()
    compare_s = []
    for url in url_list:
        resource = requests.get(url, headers=h())
        resource_text = resource.text
        soup = BeautifulSoup(resource_text, features='lxml')
        vacancy_content_list = soup.find_all('div', class_='vacancy-branded-user-content')
        for i in vacancy_content_list:
            x = str(i)
            compare_s.append(url)
            if "Django" in x or "Flask" in x or 'Python' in x:
                url_narm_jab_list.append(url)

    return


def _g_user():
    _brand_user()
    vacancy_content_g_user_d = {}
    for i in url_list:
        resource = requests.get(i, headers=h())
        resource_text = resource.text
        soup = BeautifulSoup(resource_text, features='lxml')
        vacancy_content_g_user = soup.find_all('div', class_='g-user-content')
        # vacancy_content_g_user_list = vacancy_content_g_user.find_all('div', class_='g-user-content')
        for con in vacancy_content_g_user:
            vacancy_content_g_user_d[i] = con
    for key, val in vacancy_content_g_user_d.items():
        x = str(val)
        if "Django" in x or "Flask" in x:
            url_narm_jab_list.append(key)


def final():
    _g_user()
    f_list = []
    for url in url_narm_jab_list:
        resource = requests.get(url, headers=h())
        resource_text = resource.text
        soup = BeautifulSoup(resource_text, features='lxml')
        salary_soup = soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
        company = soup.find('div', class_='vacancy-company-redesigned')
        name_soup = company.find('span', 'vacancy-company-name')
        city_1 = soup.find('div', class_='vacancy-company-redesigned')
        city = city_1.text

        if 'Москва' in city:
            city = "Москва"
        else:
            city = 'Санкт-петербург'

        salari_rep = salary_soup.text.replace("\xa0", "")
        name_rep = name_soup.text.replace("\xa0", "")

        finfl_d = {'url': url,
                   'salary': salari_rep,
                   'name': name_rep,
                   'city': city
                   }

        f_list.append(finfl_d)
    with open('dz_pars.json', 'w', encoding='utf-8') as f:
        json.dump(f_list, f, indent=4)
