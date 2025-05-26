import pandas as pd
import os
from .get_db import getConnection, getVac, closeConnection, add_rows_vacancy

from .getComp import getCompStudent
import torch

from .parseVacancy import get_all_roles, getNewVacancy


def getCleanStr(result):
  chars_to_remove = ['/', ':', ';', '(',')','.',',','–', '-', '«', '»', '_x0002_', 'ОПК', 'ПК']
  for i in chars_to_remove:
    result = result.replace(i, " ")
  result = "".join([char for char in result if not char.isdigit()])
  result = result.replace("  ", " ")
  result = result.lower()
  return result

def CleanEduProg(data):

  if type(data) is not str:
    data = " ".join(data)

  data = getCleanStr(data)

  data = data.strip()
  data = data.replace("  ", " ")
  return data

def getVacancy():
    conn = getConnection()
    data_vac = getVac(conn)
    closeConnection(conn)
    return data_vac

def getCosDistance(name_prog, value_comp, profRolesForStu, jsonRoles, jsonCity, cities):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'SBERT.pth')
    model = torch.load(model_path)
    # model = torch.load('SBERT.pth')

    # Качаем вакансии по выбранным профессиональным ролям и сравниваем с компетенциями
    per_page = 20
    number_of_pages = 5
    data = pd.DataFrame()
    for city in cities:
        code_city = jsonCity[city]
        for i in profRolesForStu:
            vacancies = get_all_roles(jsonRoles, i)
            data_t = getNewVacancy(vacancies, number_of_pages, per_page, i, code_city)
            data_t['type'] = i
            data = pd.concat([data, data_t])

    data['description_old'] = data['description']
    data = data[['name', 'description_old', 'description', 'key_skills', 'employer', 'type']]
    data['description'] = data['description'].apply(CleanEduProg)
    data['embeddings'] = [[0]] * len(data)
    data.dropna(subset=['name'], inplace=True)
    data = data.reset_index(drop=True)
    data.to_excel('result_parse.xlsx')
    add_rows_vacancy(data)

    edu_non = getCompStudent(name_prog, value_comp)
    edu = " ".join(edu_non)

    vac = data.copy()

    embeddings1 = model.encode([edu])

    for i in range(len(vac)):

        vac.at[i, 'embeddings'] = model.encode([vac.loc[i, 'description']])

        similarities = model.similarity(embeddings1, vac.loc[i, 'embeddings'])

        vac.loc[i, 'cosDist'] = f"{similarities[0][0]:.4f}"

    result = vac.sort_values(by=['cosDist'], ascending=False).drop_duplicates(subset='name').head(5)

    name = list(result['name'])

    vacancyName = list(result.index)
    cosRes = list(result['cosDist'])
    temp_l = list(result['key_skills'])

    key_skills = ', '.join([item.strip() for item in temp_l if item])
    key_skills = key_skills.split(', ')
    key_skills = list(set(key_skills))

    employer_list = []

    return(name, key_skills, employer_list, vacancyName, name_prog, edu_non, cosRes)
