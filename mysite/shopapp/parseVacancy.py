import time
import requests
import pandas as pd
import regex as re

def getListRole():
    r = requests.get('https://api.hh.ru/professional_roles').json()

    listNameRole = []

    for i in range(len(r['categories'])):
        listNameRole.append(r['categories'][i]['name'])

    return listNameRole, r

def get_url(number_of_pages, per_page, role, city):
    data=[]
    df = pd.DataFrame()
    for i in range(number_of_pages):
        while True:
            try:
                url = 'https://api.hh.ru/vacancies'
                par = {'professional_role': role, 'area': city,'per_page':per_page, 'page':i}
                r = requests.get(url, params=par)
                e=r.json()
                data.append(e)
                vacancy_details = data[0]['items'][0].keys()
                df = pd.DataFrame(columns= list(vacancy_details))
                ind = 0
                for i in range(len(data)):
                    for j in range(len(data[i]['items'])):
                        df.loc[ind] = data[i]['items'][j]
                        ind+=1
                time.sleep(0.1)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(3)
    return (list(df['name'].unique()), list(df['alternate_url']))

def clean_data(list_skills):
    clean_list = []
    if list_skills == list_skills:
        if(len(list_skills) != 0):
            for i in range(len(list_skills)):
                clean_list.append(list_skills[i]['name'])
            return ', '.join(clean_list)
        else:
            return ''
    else:
        return ''

def clean_description(a):
    return a.replace('&quot;', '')

def get_df(number_of_pages, per_page, job, name_role):
    name_vac, vah = get_url(number_of_pages, per_page, job, 1)

    # берем только цифры из ссылки вакансии
    lulu = [re.sub(r'[^0-9]', '', e) for e in vah]

    vak_url = 'https://api.hh.ru/vacancies/{}'
    # качаем вакансии по ссылкам
    var = []
    for i in range(len(lulu)):
        while True:
            try:
                var.append(requests.get(vak_url.format(lulu[i])).json())
                time.sleep(0.3)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(5)

    df = pd.DataFrame(var)
    # обработка описания вакансии
    df['description'] = df['description'].apply(lambda x: (re.sub(r'<.*?>', '', str(x))))
    df['description'] = df['description'].apply(clean_description)
    # обработка ключевых навыков
    # объединяем ключевые навыки в одну строку
    df['key_skills'] = df['key_skills'].apply(clean_data)
    df['type'] = name_role
    return df

def getNewVacancy(vacancies, number_of_pages, per_page, name_role,):
    df = get_df(number_of_pages, per_page, vacancies,name_role)
    return df

def get_all_roles(r, type):
    found_industry = next((industry for industry in r['categories'] if industry['name'] == type),
                          None)
    roles = found_industry['roles']
    all_roles = [role['id'] for role in roles]
    return all_roles