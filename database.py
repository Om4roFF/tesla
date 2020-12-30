import datetime
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
        print('exists')
    else:
        print('create')
        cursor.execute("""CREATE TABLE chat(chat_id int,student_id int, lang int, name varchar)""")
        conn.commit()


def create_lessons():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='lessons' ''')
    if cursor.fetchone()[0] == 1:
        pass
    else:
        print('create')
        cursor.execute('''CREATE TABLE lessons(student_id int, lesson_id int,datetime varchar ,status int)''')
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
    print(str(chat_id) + ' ' + str(student_id) + ' ' + str(lang) + ' ' + str(name))
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


def select_by_status(student_id):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=5)
    a = str(today - d)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    sql = f'SELECT student_id, lesson_id FROM lessons WHERE status = 0 and datetime>\'{a}\' and student_id = {student_id}'
    cursor.execute(sql)
    s = cursor.fetchall()
    conn.commit()
    return s


def select_date():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    sql = f'SELECT lesson_id,datetime FROM lessons'
    cursor.execute(sql)
    s = cursor.fetchall()
    conn.commit()
    return s


def insert_lessons(student_id, lesson_id, date_time, status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    l = select_date()
    for i in l:
        if str(i[0]) == str(lesson_id) and str(i[1]) == str(date_time):
            return -1
    sql = f'INSERT INTO lessons VALUES ({student_id},{lesson_id},\'{date_time}\',{status})'
    cursor.execute(sql)
    conn.commit()


def delete_from_lessons():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    today = datetime.datetime.now()
    d = datetime.timedelta(days=7)
    a = str(today - d)
    print(a)
    sql = f'DELETE FROM lessons WHERE datetime < \'{a}\''
    print(sql)
    cursor.execute(sql)
    conn.commit()





def update_status(student_id, lesson_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    sql = f'UPDATE lessons SET status = 1 WHERE student_id = {student_id} and lesson_id = {lesson_id}'
    print(sql)
    cursor.execute(sql)
    conn.commit()


def print_select():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    sql = f'SELECT * FROM lessons'
    cursor.execute(sql)
    s = cursor.fetchall()
    conn.commit()
    return s











