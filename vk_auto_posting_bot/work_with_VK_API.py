from importt import *
import requests

######## УЗНАЕМ ID ГРУППЫ ЧЕРЕЗ КОРОТКОЕ ИМЯ ########
async def take_ID_group(url_group, id):
    acess_token = await db_select_sys('access_token', str(id))
    response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                            params={
                                "access_token": acess_token,
                                "v": v,
                                "screen_name": url_group[15:]
                            }).json()
    return response['response']['object_id']
