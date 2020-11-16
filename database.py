import sqlite3
import os

# conn = sqlite3.connect("users.db")
# cursor = conn.cursor()
#

def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='chat' ''')
    if cursor.fetchone()[0] == 1:
        pass
    else:
        print('create')
        cursor.execute("""CREATE TABLE chat(chat_id int,student_id int, lang int, name varchar)""")
        conn.commit()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='chat' ''')
    if cursor.fetchone()[0] == 1:
        pass
    else:
        print('create ')
        cursor.execute('''CREATE TABLE homework(lesson_date varchar ,work varchar ,group varchar )''')
        conn.commit()


def insert_homework(date, homework, group):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    s = select_homework()
    for i in s:
        if i[1] == homework:
            return -1
    sql = 'INSERT INTO homework VALUES ({0},{1},{3})'.format(date, homework, group)
    cursor.execute(sql)
    conn.commit()


def insert(chat_id, student_id, lang, name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    s = select()
    for i in s:
        if str(i[0]) == str(chat_id) and str(i[1]) == str(student_id):
            return -1
    sql = 'INSERT INTO chat VALUES ({0},{1},{2},\'{3}\')'.format(chat_id, student_id, lang, name)
    print(sql)
    cursor.execute(sql)
    conn.commit()


def select():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM chat""")
    l = cursor.fetchall()
    conn.commit()
    return l


def select_by_id(chat_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM chat WHERE chat_id = {0}'.format(chat_id))
    s = cursor.fetchall()
    return s


def select_homework():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM homework''')
    l = cursor.fetchall()
    conn.commit()
    return l


def is_user(chat_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM chat WHERE chat_id = {0}'.format(chat_id))
    s = cursor.fetchall()
    return s[0][0] > 0


def delete_from_chat(chat_id, name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat WHERE chat_id = {0} and name = \'{1}\''.format(chat_id, name))
    conn.commit()