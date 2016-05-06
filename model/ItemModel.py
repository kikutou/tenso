# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class Item(object):

    def __init__(self, app):
        pass

    def getItems(self, where):
        items = DaoBase().fetchAll('mst_item', where)
        return items

    def getItem(self, where):
        item = DaoBase().fetchOne('mst_item', where)
        return item

    def addItem(self, data):

        tableName = 'mst_item'
        result = DaoBase().insertRecord(tableName, data)
        return result

    def saveItem(self, id, data):
        result = DaoBase().updateRecord('mst_item', data, id)
        return result

    def getLastJancode(self):

        result = DaoBase().fetchAll('mst_item', {'no_code_flag': 1})
        if result:
            maxValue = 0
            for key, values in result.items():

                jan_code = int(values['jan_code'])
                if jan_code > maxValue:
                    maxValue = jan_code
            maxValue = str(maxValue+1)
        else:
            maxValue = "1"
        return maxValue
