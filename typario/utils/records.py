import sqlite3


def add_value(score):
    con = sqlite3.connect("data/records.db")
    cur = con.cursor()
    query1 = f'''insert into records (value) Values ({score})'''
    cur.execute(query1)
    return


def find_record(score):
    con = sqlite3.connect("data/records.db")
    cur = con.cursor()
    query2 = '''select max(value) from records'''
    res2 = cur.execute(query2).fetchone()
    return list(res2)[0]
