# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class RelOutItem(object):

    def __init__(self, app):
        pass

    def getRelOutItems(self, where):
        relOutItems = DaoBase().fetchAll('rel_out_item', where)
        return relOutItems

    def getRelOutItem(self, where):
        relOutItem = DaoBase().fetchOne('rel_out_item', where)
        return relOutItem

    def addRelOutItem(self, data):
        tableName = 'rel_out_item'
        result = DaoBase().insertRecord(tableName, data)
        return result

    def saveRelOutItem(self, id, data):
        result = DaoBase().updateRecord('rel_out_item', data, id)
        return result