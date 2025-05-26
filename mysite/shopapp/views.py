import os
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .checkPassword import checkPassword
from .getComp import getListCopm
from .getResult import getCosDistance
from .get_db import addUser, getResInfo, update_table_EduProgram, add_rows_EduProgram, getConnection, closeConnection, \
    getEduProg, get_Users, get_edu_table, drop_rows
import pandas as pd
from datetime import datetime

from .parseVacancy import getListRole, getAreas


def index(request):
    request.session['logged'] = 0
    listNameRole, r = getListRole()
    request.session['listNameRole'] = listNameRole
    request.session['jsonRoles'] = r
    areas, dict_globalArea = getAreas()

    dictionary_area = {}
    for i in range(len(areas)):
        if (areas[i][0] == '113'):
            dictionary_area[areas[i][3]] = int(areas[i][2])

    z = dictionary_area | dict_globalArea
    z = dict(sorted(z.items()))
    z['Россия'] = 113

    request.session['jsonRegion'] = z
    choices = list(z.keys())


    context = {
        'name_prog': get_edu_table(),
        'roles': listNameRole,
        'regions': choices
    }
    drop_rows()
    return render(request, 'shopapp/index.html', context)


def button_click_view(request):
    if request.method == 'POST':
        # Обработка нажатия кнопки
        request.session['email'] = request.POST.get("email")
        request.session['placeOfWork'] = request.POST.get("placeOfWork")
        request.session['post'] = request.POST.get("post")
        request.session['NameProg'] = request.POST.get("selectNameProg")
        request.session['user'] = request.POST.get("selectNameProg")

        request.session['region'] = request.POST.getlist("regions[]")

        request.session['profRolesForStu'] = request.POST.getlist("roles[]")
        if((len(request.POST.getlist("roles[]"))!=0) & (len(request.POST.getlist("regions[]"))!=0)):
            return HttpResponseRedirect('pageTest')
        else:
            return HttpResponse("Заполните все поля!")




def button_click_view_2(request):
    if request.method == 'POST' and 'button_name_2' in request.POST:
        num_comp = []
        for i in range(request.session['lenNameComp']):
            num_comp.append(request.POST.get(str(i)))
        request.session['valueComp'] = num_comp
        return HttpResponseRedirect('resultPage')
    return HttpResponse('')


def button_click_view_3(request):
    if request.method == 'POST':
        rating = []
        name_radio = ['rating0', 'rating1', 'rating2', 'rating3', 'rating4']
        for i in name_radio:
            rating.append(request.POST.get(i))
        request.session['rating'] = rating

        # Получаем текущие дату и время
        now = datetime.now()
        addUser(email=request.session.get('email', None),
                placeOfWork=request.session.get('placeOfWork', None),
                post=request.session.get('post', None),
                programCode=request.session.get('programCode', None),
                programEduName=request.session.get('user', None),
                studentComp=str(request.session.get('student_comp', None)),
                vacancyName=str(request.session.get('name_vac', None)),
                indexVac=str(request.session.get('index_vac', None)),
                rateStudent=str(request.session.get('rating', None)),

                profRolesForStu=str(request.session.get('profRolesForStu', None)),
                region=str(request.session.get('region', None)),
                cosRes=str(request.session.get('cosRes', None)),

                dateAdded=str(now.strftime("%Y-%m-%d %H:%M:%S")))

        # Создание DataFrame
        data = {
            'email': [request.session.get('email', None)],
            'placeOfWork': [request.session.get('placeOfWork', None)],
            'post': [request.session.get('post', None)],
            'name_prog': [request.session.get('user', None)],
            #ключ и значение, которое будет возвращено, если значения по ключу нет
            'student_comp': [request.session.get('student_comp', None)],
            'name_vac': [request.session.get('name_vac', None)],
            'index_vac': [request.session.get('index_vac', None)],
            'rating': [request.session.get('rating', None)],
            'cosRes': [request.session.get('cosRes', None)]
        }
        drop_rows()
        return render(request, 'shopapp/finallPage.html')
    return HttpResponse('')


def pageTest(request):
    l_comp, program_code = getListCopm(request.session.get('NameProg'))
    request.session['programCode'] = program_code[0]
    name_comp_list = []
    for i in range(len(l_comp)):
        name_comp_list.append((i, '1', '0', l_comp[i]))
    context = {
        'name_comp': name_comp_list,
    }
    request.session['lenNameComp'] = len(name_comp_list)

    return render(request, 'shopapp/pageTest.html', context)


def resultPage(request):
    name, key_skills, employer_list, vacancyName, name_prog, edu, cosRes = getCosDistance(request.session['NameProg'],
                                                                                          request.session['valueComp'],
                                                                                          request.session['profRolesForStu'],
                                                                                          request.session['jsonRoles'],
                                                                                          request.session['jsonRegion'],
                                                                                          request.session['region']
                                                                                         )
    description_vac = getResInfo(vacancyName)

    rating_num_description_vac = []
    for i in range(len(description_vac)):
        rating_num_description_vac.append(('rating' + str(i), name[i], description_vac[i]))

    context = {
        'name': name,
        'key_skills': key_skills,
        'employer_list': employer_list,
        'rating_num_description_vac': rating_num_description_vac,
        'student_comp': edu
    }

    request.session['student_comp'] = edu
    request.session['name_vac'] = name
    request.session['index_vac'] = vacancyName
    request.session['cosRes'] = cosRes
    return render(request, 'shopapp/resultPage.html', context)


def finallPage(request):
    return render(request, 'finallPage.html')


def pageEnter(request):
    return render(request, 'shopapp/pageEnter.html')


def button_enter_click(request):
    if request.method == 'POST':
        if ((request.POST.get("login") == 'admin') & ((checkPassword(request.POST.get("password")) == 1))):
            request.session['logged'] = 1
            return HttpResponseRedirect('addProgram')
        if (request.POST.get("login") != 'admin'):
            context = {'error_message': 'Неверный логин.'}
            return render(request, 'shopapp/pageEnter.html', context)
        if (checkPassword(request.POST.get("password")) == 0):
            context = {'error_message': 'Неверный пароль.'}
            return render(request, 'shopapp/pageEnter.html', context)

    else:
        return HttpResponse('')


def addProgram(request):
    if (request.session.get('logged', None) == 1):
        conn = getConnection()
        data_edu = getEduProg(conn)
        closeConnection(conn)

        data_edu.rename(
            columns={'code': 'Код', 'name_prog': 'Наименование программы', 'name_comp': 'Наименование компетенции'},
            inplace=True)

        data_edu = data_edu[['Код', 'Наименование программы', 'Наименование компетенции']]

        html_table = data_edu.to_html()
        context = {'html_table': html_table}
        return render(request, 'shopapp/pageAddProgram.html', context)
    else:
        return HttpResponseRedirect('pageEnter')


def upload_file(request):
    if request.method == 'POST' and 'button_update' in request.POST:
        try:
            file = request.FILES['file']
        except:
            return HttpResponse("Выберите файл для загрузки!")
        # Обработка файла
        # Например, сохранение файла
        with open('file.xlsx', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Логика обновления данных
        df = pd.read_excel('file.xlsx')
        update_table_EduProgram(df)
        # Удаляем временный файл
        os.remove('file.xlsx')

        return HttpResponse("Таблица обновлена!")

    if request.method == 'POST' and 'button_add' in request.POST:
        try:
            file = request.FILES['file']
        except:
            return HttpResponse("Выберите файл для загрузки!")
        # Обработка файла
        # Например, сохранение файла
        with open('file.xlsx', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Логика обновления данных
        df = pd.read_excel('file.xlsx')
        add_rows_EduProgram(df)
        # Удаляем временный файл
        os.remove('file.xlsx')

        return HttpResponse("Данные добавлены!")
    return render(request, 'pageAddProgram.html')

def pageResultReport(request):
    if (request.session.get('logged', None) == 1):
        data = get_Users()
        data = data.drop(columns=['id'])
        data = data.drop(columns=['Индексы вакансий'])
        html_table = data.tail(100).iloc[::-1].to_html()
        context = {'html_table': html_table}
        return render(request, 'shopapp/pageResultReport.html', context)
    else:
        return HttpResponseRedirect('pageEnter')


def download_results(request):
    df = get_Users()
    # Создание буферного объекта для сохранения Excel файла
    buffer = BytesIO()

    # Запись DataFrame в Excel файл
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Перемещение указателя в начало буфера
    buffer.seek(0)

    # Формирование HTTP ответа с прикрепленным Excel файлом
    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reportTestStudents.xlsx"'

    return response
