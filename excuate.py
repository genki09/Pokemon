# -*-coding:gbk-*-

import mysql.connector
import pymysql

host = "localhost"
user_name = "root"
password = "1qw23e00"
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
    #   �ú���ʵ����ȡ�����ݿ�ݽ��������ݿⷵ�ص�ֵ����Ϊ��ѯ��䷵�صĲ�ѯ����ȣ�
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
    #   �ú���ʵ�������ݿ�ݽ���䣬������ֵ�������������ݿ���ӻ�ɾ��Ԫ�أ�
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
