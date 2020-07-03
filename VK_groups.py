import requests
import time
import json

def get_unique_groups(user_id, token, file_name):
    
    params1 = {
        'access_token': token,
        'user_id': user_id,
        'v': '5.110'
    }
    resp1 = requests.get(url='https://api.vk.com/method/groups.get/', params= params1)
    resp2 = requests.get(url= 'https://api.vk.com/method/friends.get', params= params1)
    group_id_set = set(resp1.json()['response']['items'])
    count1 = 0
    for friends in resp2.json()['response']['items']:
        print(f'Идёт проверка групп пользователя # {count1 + 1}')
        params2 = {
            'access_token': token,
            'user_id': friends,
            'v': '5.110',
        }
        resp3 = requests.get(url= 'https://api.vk.com/method/groups.get/', params= params2)
        try:
            group_id_set.difference_update(set(resp3.json()['response']['items']))
        except Exception as e:
            print(resp3.json()['error']['error_msg'])
        count1 += 1
        time.sleep(1.0)
    to_json = []
    for groups in group_id_set:
        params3 = {
            'access_token': token,
            'group_id': groups,
            'v': '5.110',
            'fields' : 'members_count'
        }
        resp4 = requests.get(url= 'https://api.vk.com/method/groups.getById', params= params3)
        groups = {'name': resp4.json()['response'][0]['name'],
                  'id': groups,
                  'members_count': resp4.json()['response'][0]['members_count']
                  }
        to_json.append(groups)
        time.sleep(1.0)
    with open(file_name, 'w', encoding= 'utf-8') as fw:
        json.dump(to_json, fw,  ensure_ascii= False, indent = 4)
    return file_name

get_unique_groups('171691064',
                  '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
                  'json_test_1'
                  )
