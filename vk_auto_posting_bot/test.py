
# from importt import *
import requests

######## УЗНАЕМ ID ГРУППЫ ЧЕРЕЗ КОРОТКОЕ ИМЯ ########
def a():
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                "access_token": 'vk1.a.ScJhTV9EEcNbZFMA4rjNbRf5kmlJdFWlBFBl3nfAH8WCrDjO0ACgbd-33z1IETJTg3FS4ZO5eEwQrQ_Yc5repuynBkqnfLEBtjojdfGDL15Uo1Wf_AawJCV4wDcrZe1cCJG7zHzbUyps0cvDPY-TQiFdyVNcWIxH7lvjoG7doxVcYFwpthHHtksK0-qy9hf_',
                                "v": 5.131,
                                "domain": 'bmwdriv',
                                "count": 100
                            }).json()['response']['items']
    print(response)
a()