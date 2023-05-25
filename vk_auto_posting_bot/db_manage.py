import sqlite3 as sq
from importt import pat
async def db_update(pole, id, text, sys):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"UPDATE users SET {str(pole)} = (?) WHERE chat_id == '{str(id)}' AND systemes == '{str(sys)}'", (str(text),))
        con.commit()

async def db_select(pole, id):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {str(pole)} FROM users WHERE chat_id == '{str(id)}'")
        return sql.fetchone()

async def db_select_2(system, id):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM users WHERE chat_id == '{str(id)}' AND systemes == '{system}'")
        return sql.fetchall()

async def db_select_all(sys, id):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {sys} FROM users WHERE chat_id == '{str(id)}'")
        return sql.fetchall()

async def db_select_with_sys(pole, id, sys):
    with sq.connect(f'{pat}db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {str(pole)} FROM users WHERE chat_id == '{str(id)}' AND systemes == '{str(sys)}'")
        return sql.fetchall()

async def db_select_id_sys(pole):
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {str(pole)} FROM sys")
        return sql.fetchall()

async def db_update_txt_o(id):
    with sq.connect(f'{pat}db_sys.db') as conn:
        sql = conn.cursor()
        sql.execute(f"UPDATE sys SET txt = (?) WHERE chat_id == '{str(id)}'","o",)
        conn.commit()

async def db_update_sys(pole, id, text):
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute(f"UPDATE sys SET {str(pole)} = (?) WHERE chat_id == '{str(id)}'", (str(text),))
        con.commit()

async def db_select_sys(pole, id):
    with sq.connect(f'{pat}db_sys.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {str(pole)} FROM sys WHERE chat_id == '{str(id)}'")
        return sql.fetchone()