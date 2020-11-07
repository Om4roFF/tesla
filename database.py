import sqlite3
import os

conn = sqlite3.connect("users.db")
cursor = conn.cursor()


def create_table():
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
    s = select_homework()
    for i in s:
        if i[1] == homework:
            return -1
    sql = 'INSERT INTO homework VALUES ({0},{1},{3})'.format(date, homework, group)
    cursor.execute(sql)
    conn.commit()


def insert(chat_id, student_id, lang, name):
    s = select()
    for i in s:
        if i[0] == chat_id:
            return -1
    sql = 'INSERT INTO chat VALUES ({0},{1},{2},\'{3}\')'.format(chat_id, student_id, lang, name)
    print(sql)
    cursor.execute(sql)
    conn.commit()


def select():
    cursor.execute("""SELECT * FROM chat""")
    l = cursor.fetchall()
    conn.commit()
    return l


def select_homework():
    cursor.execute('''SELECT * FROM homework''')
    l = cursor.fetchall()
    conn.commit()
    return l



def is_user(chat_id):
    cursor.execute('SELECT COUNT(*) FROM chat WHERE chat_id = {0}'.format(chat_id))
    s = cursor.fetchall()
    return s[0][0] > 0

# create_table()
# insert(1234, 2314,1,"hbhhbhb")
# l = select()
# print(l)
