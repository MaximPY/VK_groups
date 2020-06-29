import requests
import time
# (eshmargunov) и id (171691064)
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
params1 = {
    'access_token': token,
    'user_id': '171691064',
    'v': '5.110'
}
resp1 = requests.get(url='https://api.vk.com/method/groups.get/', params= params1)
resp2 = requests.get(url= 'https://api.vk.com/method/friends.get', params= params1)
group_id_list = resp1.json()['response']['items']
friend_list = resp2.json()['response']['items']
count1 = 0
count2 = 0
needed_groups_list = []
for friends in friend_list:
    print(f'Идёт проверка групп пользователя # {count1 + 1}')
    user_id = friends
    params2 = {
        'access_token': token,
        'user_id': user_id,
        'v': '5.110',
    }
    resp3 = requests.get(url= 'https://api.vk.com/method/groups.get/', params= params2)
    try:
        if group_id_list[count2] in resp3.json()['response']['items']:
            count2 += 1
            pass
        else:
            if group_id_list[count2] not in needed_groups_list:
                needed_groups_list.append(group_id_list[count2])
    except Exception as e:
        print(resp3.json()['error']['error_msg'])
        # print(f'Пользователь с id {friends} ограничил доступ к своему профилю')
    count1 += 1
    time.sleep(1.0)
print(needed_groups_list)
