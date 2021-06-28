# -*-coding:gbk-*-

import mysql.connector
import pymysql

host = "localhost"
user_name = "root"
password = ""
database = "pokeDex"


def cal_pym(char):
    conn = pymysql.connect(
        host=host,
        user=user_name,
        password=password,
        database=database)

    cursor = conn.cursor()
    cursor.execute(char)
    conn.commit()



def cal_r(char):
    #   该函数实现提取向数据库递交语句后数据库返回的值（多为查询语句返回的查询结果等）
    mydb = mysql.connector.connect(
        host=host,
        user=user_name,
        passwd=password,
        database=database,
        auth_plugin='mysql_native_password')

    mycursor = mydb.cursor()
    mycursor.autocommit = True
    mycursor.execute(char)

    return mycursor.fetchall()


def cal_nr(char):
    #   该函数实现向数据库递交语句，不返回值（多用于向数据库添加或删除元素）
    mydb = mysql.connector.connect(
        host=host,
        user=user_name,
        passwd=password,
        database=database)

    mycursor = mydb.cursor()
    mycursor.autocommit = True
    mycursor.execute(char)
    mydb.commit()


def fet_list(column, db):
    find = cal_r("SELECT %s FROM %s" % (column, db))
    y = []
    for x in find:
        y.append(x[0])
    return y
