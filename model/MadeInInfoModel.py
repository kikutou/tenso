# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class MadeInInfo(object):

    def __init__(self, app):
        pass

    def getMadeInInfos(self, where):
        madeInInfos = DaoBase().fetchAll('mst_made_in', where)
        return madeInInfos

    def getMadeInInfo(self, where):
        madeInInfo = DaoBase().fetchOne('mst_made_in', where)
        return madeInInfo

    def addMadeInInfo(self, data):

        tableName = 'mst_made_in'
        result = DaoBase().insertRecord(tableName, data)
        return result

    def saveMadeInInfo(self, id, data):
        result = DaoBase().updateRecord('mst_made_in', data, id)
        return result