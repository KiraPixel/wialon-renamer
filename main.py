import csv
import json
import requests

api_url = 'https://hst-api.wialon.com/wialon/ajax.html?'
token = ''


def get_wialon_sid():
    params = {
        'token': token
    }
    response = requests.get(api_url, params={
        'svc': 'token/login',
        'params': json.dumps(params)
    })

    if response.status_code == 200:
        result = response.json()
        if 'eid' in result:
            return result['eid']
        else:
            print(f"Error: {result}")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def search_wialon_objects(sid):
    params = {
        'spec': {
            'itemsType': 'avl_unit',
            'propName': 'sys_name',
            'propValueMask': '*',
            'sortType': 'sys_name'
        },
        'force': 1,
        'flags': 1,
        'from': 0,
        'to': 0,
    }
    response = requests.get(api_url, params={
        'svc': 'core/search_items',
        'params': json.dumps(params),
        'sid': sid
    })

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def edit_transport(sid, id, new_name):
    params = {
        "itemId": id,
        "name": new_name
    }
    response = requests.get(api_url, params={
        'svc': 'item/update_name',
        'params': json.dumps(params),
        'sid': sid
    })

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def save_objects_to_csv(objects, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'uNumber'])  # Заголовки столбцов

        for obj in objects['items']:
            if isinstance(obj, dict):  # Проверка на правильный тип данных
                item_id = obj['id']
                u_number = obj['nm']
                writer.writerow([item_id, u_number])
            else:
                print(f"Skipping invalid object: {obj}")  # Отладочная информация


def change_names_from_csv(sid, csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                item_id = row[0].strip()
                new_name = row[1].strip()
                result = edit_transport(sid, item_id, new_name)
                if result:
                    print(f"Successfully changed name of item {item_id} to {new_name}")
                else:
                    print(f"Failed to change name of item {item_id}")
            else:
                print(f"Invalid data in row: {row}")


sid = get_wialon_sid()

# change_names_from_csv(sid, 'new_data.csv')
# transport = search_wialon_objects(sid)
# print(transport)
# edit_transport(sid, 22681762, 'R 00583')
