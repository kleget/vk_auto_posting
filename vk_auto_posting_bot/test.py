import time


def day_to_sec(day):# возвраящает дни в секундах
    return day*60*60*24+3600*3

print(time.time() + day_to_sec(31))