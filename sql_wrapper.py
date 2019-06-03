# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 13:05:04 2019

@author: swang
"""
class sqlthefuk(object):
    """
    
    sql helper to simplify the query generating process, which is a super 
    painful work to do 
    """
    def __init__(self):
        self.query = ""
    
    def wrapit(self, item):
        # add left and right parenthesis
        return "(" + item + ")"
    
    def select(self, columns, table, nested_mark=''):
        # select multiple columns
        if isinstance(columns, list):
            if not nested_mark:
                columns = ', '.join(columns)
            else:
                columns = ', '.join([nested_mark + '.' + c for c in columns])
        
        # select single column
        elif isinstance(columns, str):
            pass
        
        # se;ect all columns
        elif not columns:
            columns = '*'

        if not nested_mark:
            return "select {} from {}".format(columns, table)
        else:
            query = "select {} from {} {}".format(columns, table, nested_mark)
            return self.wrapit(qry)