import json
import requests
import config
import csv


"""

"""

# конкретно для программы нам нужны только ИНН и Description
def get_partner_list_from_1c():
    """Через ОДата получаем список контрагентов"""
    payload = {}
    headers = {'Authorization':config.auth_header}

    get_url = config.retail_url
    response = requests.request("GET", get_url, headers=headers, data=payload)
    todos = json.loads(response.text)

    partner_list = []
    for el in todos['value']:
        # если партнер из группы Покупатели
        if (el['Parent_Key'] == "f70ace00-a231-11e9-83a1-005056c00008"):
            partner_list.append(el)
    
    with open('output.csv', 'w', newline='') as csvfile:
        field_names = ['Code','Имя', 'Описание', 'ИНН', 'Parent_Key']
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        for el in partner_list:
            code = el['Code']
            name = el['НаименованиеПолное']
            description = el['Description']
            inn = el['ИНН']
            parent_key = el['Parent_Key']
            row = {'Code':code, 'Имя':name, 'Описание':description, 'ИНН':inn, 'Parent_Key':parent_key}
            writer.writerow(row)
    
    return partner_list

#get_partner_list_from_1c()