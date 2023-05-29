import os, time
from config import *
import sqlite3 as sq

#ВОЗРАЩАЕТ КОЛЛИЧЕСТВО СИСТЕМ В ТАБЛИЦЕ
def parsing_google_sheets_1():
    try:
        with sq.connect(f'{pat}db_main.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT COUNT(*) FROM users")
            a = sql.fetchall()
            return a[0][0]
    except:
        time.sleep(0.01)
        parsing_google_sheets_1()

#ВОЗРАЩАЕТ ПАРАМЕТРЫ
def parsing_google_sheets_2(num):
    try:#
        with sq.connect(f'{pat}db_main.db') as con:
            sql = con.cursor()
            sql.execute(f"SELECT * FROM users")
            b = sql.fetchall()
        b[int(num)] = b[int(num)][3::]
        if b[int(num)][0] == 'OFF' or b[int(num)][0] is None or b[int(num)][0] == '':
            return 'STOP'
        if b[int(num)][1] == 'empty' or b[int(num)][4] == 'empty' or b[int(num)][8] == 'empty':
            return 'STOP'
        else:
            b[int(num)] = [*b[int(num)]]
            del b[int(num)][0]
            while '' in b[int(num)]:
                b[int(num)].remove('')
        for u in range(len(b[num])):
            if u not in [0, 1, 2, 3, 4, 5, 6]:
                params = open('params.txt', 'a')
                if b[num][u] != 'empty':
                    prt = b[num][u][15:]
                    prt_r = b[num][0]
                    params.write(f'{how_many_posts_do_we_make} {prt} {prt_r}\n') ######## tyt
                    params.close()
                else:
                    break
        if len(b[num]) >= 0:
            with sq.connect(f'{pat}db_sys.db') as con:
                sql = con.cursor()
                sql.execute(f"SELECT access_token FROM sys WHERE chat_id == '{str(b[num][6])}'")
                token = sql.fetchone()[0]

            if b[num][1] != 'empty':
                b[num][1] = b[num][1].split('+')
            if b[num][2] != 'empty':
                b[num][2] = b[num][2].split('+')
            return [b[num][1],
                    b[num][2],
                    b[num][3][15:], #
                    b[num][4],#
                    token,
                    b[num][5]]
    except:
        time.sleep(0.01)
        parsing_google_sheets_2(num)
