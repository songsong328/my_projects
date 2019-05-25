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
    print("Connected to Database.\n")
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

def add_col(tblname, df, col_name, co):
    col = df[col_name]
    try:
        qry = "ALTER TABLE {} ADD COLUMN {} VARCHAR".format(tblname, col_name)
        co.cursor().execute(qry)
        print("Successfully Added Column {} to {}".format(col_name, tblname))
    except:
        print("Failed to Add Column {}".format(col_name))
    
    sql = """INSERT INTO {} ({}) VALUES """.format(tblname, col_name)
    incremental = 0
    length = col.shape[0]
    data = sql
    
    progress_count = 0
    for row in range(col.shape[0]):
        val = ["\'" + col.iloc[row] + "\'"]
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
            try:
                progress_count += incremental
                co.cursor().execute(data)
                print("{:.0f}% done\n".format(progress_count*100/col.shape[0]))
            except:
                print("Failed, Rolled Back.\n")
                rollback()
                rollback()
                
            incremental = 0
            data = sql    

def drop_tbl(tblname, co):
    sql = """DROP TABLE {}""".format(tblname)
    co.cursor().execute(sql)
    print("Successfully Dropped Table {}".format(tblname))
    co.commit()

def drop_col(tblname, col_name, co):
    sql = """ALTER TABLE {} DROP COLUMN {}""".format(tblname, col_name)
    co.cursor().execute(sql)
    print("Successfully Dropped Column {} from {}".format(col_name, tblname))
    co.commit()

def rollback(co):
    c = conndb()
    c.rollback()
    c.commit()

def upload_table(tblname, df, co):
    # name correction
    df_cols = []
    for x in df.columns:
        if x[0].isdigit():
            newx = input("correction: {} starting with a number\n".format(x))
            while newx[0].isdigit() or len(newx) > 30:
                newx = input("correction: {} starting with a number".format(x))
            df_cols += [newx]
            continue
        if len(x) > 30:
            newx = input("correction: {} too long\n".format(x))
            while len(newx) > 30:
                newx = input("correction: {} too long".format(x))
            df_cols += [newx]
            continue
        df_cols += [x]
    
    # create table template
    create_tbl(tblname, df_cols, co)
    
    # insert into database
    sql = """INSERT INTO {} VALUES """.format(tblname)
    df.columns = df_cols
    todo = df.astype(str).copy()
    length = todo.shape[0]
    incremental = 0
    data = sql
    
    # track progress
    progress_count = 0
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
            try:
                co.cursor().execute(data)
                progress_count += incremental
                print("{:.0f}% done\n".format((progress_count/length)*100))
            except:
                print("Failed, Rolled Back.\n")
                rollback()
                rollback()
            incremental = 0
            data = sql
    co.commit()
