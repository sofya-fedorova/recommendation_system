import sqlite3
import pandas as pd

def getConnection():
    connection = sqlite3.connect('recommendation_system.db')
    return connection

def getVac(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Vacancy')
    data_vac = cursor.fetchall()
    data = pd.DataFrame(data_vac)
    data.rename(columns={0: 'name', 1: 'description_old', 2: 'description', 3: 'key_skills', 4: 'employer', 5: 'type', 6:'embeddings'}, inplace=True)
    return(data)

def getEduProg(connection):
    cursor = connection.cursor()
    # Выбираем активных пользователей
    cursor.execute('SELECT * FROM EduProgram')
    data_edu = cursor.fetchall()
    data = pd.DataFrame(data_edu)
    data.rename(columns={0: 'code', 1: 'name_prog', 2: 'name_comp', 3: 'ind'}, inplace=True)
    return(data)

def closeConnection(connection):
    return connection.close()

def getResInfo(vacancyName):
    connection = getConnection()
    vac = getVac(connection) #получим все вакансии и выберем из них по индексу описание по рекомендованным профессиям
    temp_df = vac.loc[vacancyName] #временный датафрейм с выбранными по индексам записями

    return list(temp_df['description_old'])


def addUser(email='email', placeOfWork='place', post='post', programCode='progCode', programEduName='eduName', studentComp='studentComp', vacancyName='vacancyName',indexVac='test', rateStudent=0, dateAdded='test'):
    connection = getConnection()
    cursor = connection.cursor()
    user_data = (email, placeOfWork, post, programCode, programEduName, studentComp, vacancyName, indexVac, rateStudent, dateAdded)
    insert_query = """INSERT INTO users (email, placeOfWork, post, programCode,
     programEduName, studentComp, vacancyName, indexVac, rateStudent, dateAdded) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(insert_query, user_data)
    connection.commit()
    closeConnection(connection)

def update_table_EduProgram(data):
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM EduProgram;")
    connection.commit()

    data.to_sql('EduProgram', connection, if_exists='append', index=False)

    closeConnection(connection)

def add_rows_EduProgram(data):
    connection = getConnection()
    data.to_sql('EduProgram', connection, if_exists='append', index=False)
    closeConnection(connection)

def add_rows_vacancy(data):
    connection = getConnection()
    data = data[['name', 'description_old', 'description', 'key_skills', 'employer', 'type', 'embeddings']]
    data['type'] = data['type'].astype(str)
    # data['key_skills'].fillna('-', inplace=True)
    data.fillna({'key_skills': '-'}, inplace=True)
    data['employer'] = data['employer'].astype(str)
    data['embeddings'] = data['embeddings'].astype(str)
    data.to_sql('Vacancy', connection, if_exists='append', index=False)
    closeConnection(connection)

def clean_table_vacancy():
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Vacancy;")
    connection.commit()

    closeConnection(connection)

def get_Users():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    data_vac = cursor.fetchall()
    data = pd.DataFrame(data_vac)
    data.rename(columns={0: 'id', 1: 'email', 2: 'Образовательное учреждение', 3: 'Уровень образования', 4: 'Код программы',
                         5: 'Наименование программы', 6: 'Компетенции студента',
                         7: 'Наименования вакансий', 8: 'Индексы вакансий', 9: 'Рейтинг', 10: 'Дата'}, inplace=True)
    return (data)

def get_edu_table():
    conn = getConnection()
    data_edu = getEduProg(conn)
    closeConnection(conn)
    list_name = data_edu['name_prog'].unique()
    return(list_name)

def drop_rows():
    conn = getConnection()
    cursor = conn.cursor()
    # Удалить записи
    cursor.execute("DELETE FROM Vacancy;")
    conn.commit()