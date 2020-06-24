import requests
# (eshmargunov) и id (171691064)
params1 = {
    'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
    'user_id': '171691064',
    'v': '5.110'
}
resp1 = requests.get(url='https://api.vk.com/method/groups.get/', params= params1)

group_id_list = resp1.json()['response']['items']
# print(id_list)
# print(resp.json())

params2= {
    'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
    'group_id': group_id_list[0],
    'v': '5.110',
    'fields': '',
    'filter': 'friends'

}
resp2 = requests.get(url= 'https://api.vk.com/method/groups.getMembers', params= params2)

print(resp2.json())

