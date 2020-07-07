import requests
import time
import json


def get_raw_group_set(params):
    resp1 = requests.get(url='https://api.vk.com/method/groups.get/', params=params)
    raw_group_id_set = set(resp1.json()['response']['items'])
    return raw_group_id_set


def get_friend_list(params):
    resp2 = requests.get(url='https://api.vk.com/method/friends.get', params=params)
    friend_list = resp2.json()['response']['items']
    return friend_list


def get_groups_set(base_params, friend_list, group_id_set):
    count = 0
    params = base_params.copy()
    backup_params = base_params.copy()
    for friends in friend_list:
        print(f'Идёт проверка групп пользователя # {count1 + 1}')
        params['user_id'] = friends
        resp3 = requests.get(url='https://api.vk.com/method/groups.get/', params=params)
        try:
            group_id_set.difference_update(set(resp3.json()['response']['items']))
        except Exception as e:
            if resp3.json()['error']['error_code'] == 6:
                time.sleep(2.0)
                backup_params['user_id'] = resp3.json()['error']['request_params'][0]['value'],
                backup_resp = requests.get(url='https://api.vk.com/method/groups.get/', params=backup_params)
                try:
                    group_id_set.difference_update(set(backup_resp.json()['response']['items']))
                except Exception as ex:
                    print(backup_resp.json()['error']['error_msg'])
            else:
                print(resp3.json()['error']['error_msg'])
        count += 1
    return group_id_set


def get_pre_json_list(base_params, group_id_set):
    to_json = []
    params = base_params.copy()
    for groups in group_id_set:
        params['group_id'] = groups
        params['fields'] = 'members_count'
        resp4 = requests.get(url='https://api.vk.com/method/groups.getById', params=params)
        groups = {'name': resp4.json()['response'][0]['name'],
                  'id': groups,
                  'members_count': resp4.json()['response'][0]['members_count']
                  }
        to_json.append(groups)
        time.sleep(0.5)
    return to_json


def write_file_json(to_json, file_name):
    with open(file_name, 'w', encoding='utf-8') as fw:
        json.dump(to_json, fw, ensure_ascii=False, indent=4)
    return


def get_unique_groups(user_id=input('Введите user id '), token=input('Введите token '),
                      file_name=input('Введите название файла ')):
    base_params = {
        'access_token': token,
        'user_id': user_id,
        'v': '5.110'
    }
    try:
        needed_set = get_raw_group_set(base_params)
    except Exception as e:
        if resp1.json()['error']['error_code'] == 5:
            print('Введен неверный токен')
            return
        elif resp1.json()['error']['error_code'] == 100:
            print('Введён неверный формат данных токена или id')
            return
    friend_list = get_friend_list(base_params)
    final_set = get_groups_set(base_params, friend_list, needed_set)
    time.sleep(2.0)
    pre_json = get_pre_json_list(base_params, final_set)
    write_file_json(pre_json, f'{file_name}')
    return


get_unique_groups()
