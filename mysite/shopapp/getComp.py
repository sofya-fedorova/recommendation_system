from .get_db import getConnection, getEduProg, closeConnection


def getCleanStr(result):
  chars_to_remove = ['.','–', '-', '_x0002_', 'ОПК', 'ПК', 'SS', 'КК']
  for i in chars_to_remove:
    result = result.replace(i, " ")
  result = "".join([char for char in result if not char.isdigit()])
  result = result.replace("  ", " ")
  result = result.strip()
  return result

def getListCopm(nameProg):
    conn = getConnection()
    data_edu = getEduProg(conn)
    closeConnection(conn)

    # data_edu = pd.read_excel('C:/Users/мвм/ДИПЛОМ2/данные по образовательным программам.xlsx')
    program_code = list(
        data_edu[data_edu['name_prog'] == nameProg]['code'].unique())

    name_komp = list(
        data_edu[data_edu['name_prog'] == nameProg]['name_comp'].unique())

    for i in range(len(name_komp)):
        name_komp[i] = getCleanStr(name_komp[i])

    return name_komp, program_code


def getCompStudent(name_prog, value_comp):
    list_comp, code = getListCopm(name_prog)
    result_list_comp = []
    for i in range(len(list_comp)):
        if(int(value_comp[i]) == 1):
            result_list_comp.append(list_comp[i])
    return result_list_comp
