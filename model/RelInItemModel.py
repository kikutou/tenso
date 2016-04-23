# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class RelInItem(object):

    def __init__(self, app):
        pass

    def getRelInItems(self, where):
        relInItems = DaoBase().fetchAll('rel_in_item', where)
        return relInItems

    def getRelInItem(self, where):
        relInItem = DaoBase().fetchOne('rel_in_item', where)
        return relInItem

    def addRelInItem(self, data):

        tableName = 'rel_in_item'
        result = DaoBase().insertRecord(tableName, data)
        return result

    def saveRelInItem(self, id, data):
        result = DaoBase().updateRecord('rel_in_item', data, id)
        return result