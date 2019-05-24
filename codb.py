# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import psycopg2

def conndb():
    connection = psycopg2.connect(user = "postgres",
                              password = "555328",
                              host = "localhost",
                              port = "5432",
                              database = "songdb")
    return connection

def create_tbl(tblname, columns, co):
    sql = """CREATE TABLE {} (\n""".format(tblname)
    for i, name in enumerate(columns):
        if i+1 < len(columns):
            sql += "{} VARCHAR(1000),\n".format(name)
        else:
            sql += "{} VARCHAR(1000))".format(name)
    
    co.cursor().execute(sql)
    co.commit()

def drop_tbl(tblname, co):
    sql = """DROP TABLE {}""".format(tblname)
    co.cursor().execute(sql)
    co.commit()

def rollback():
    c = conndb()
    c.rollback()
    c.commit()

def upload_table(tblname, df, co):
    create_tbl(tblname, df.columns.tolist(), co)
    
    sql = """INSERT INTO {} VALUES """.format(tblname)
    todo = df.astype(str).copy()
    length = todo.shape[0]
    incremental = 0
    data = sql
    for row in range(length):
        val = ["\'{}\'".format(x) for x in todo.iloc[row]]
        incremental += 1
        header = "("
        footer = "),\n"

        if row+1 < length:
            data += (header + 
                     ', '.join(val) +
                     footer)
        else:
            data += (header +
                     ', '.join(val) +
                     ")\n")
        if (incremental > 999) or (length - (row+1) == 0):
            co.cursor().execute(data)
            incremental = 0
            data = sql
    co.commit()
            