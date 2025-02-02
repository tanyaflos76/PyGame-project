import sqlite3


def init_db() -> None:
    con = sqlite3.connect("data/records.db")
    cur = con.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS records (
        value INT
    )
    """
    cur.execute(query)
    con.commit()


def add_value(score: int) -> None:
    con = sqlite3.connect("data/records.db")
    cur = con.cursor()
    query = f"""insert into records (value) Values ({score})"""
    cur.execute(query)
    con.commit()
    con.close()


def find_record() -> int:
    con = sqlite3.connect("data/records.db")
    cur = con.cursor()
    query = """select max(value) from records"""
    res = cur.execute(query).fetchone()
    con.close()
    return list(res)[0]
