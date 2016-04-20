# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class Inbox(object):

    def __init__(self, app):
        pass

    def getInboxDatas(self, where):
        inboxDatas = DaoBase().fetchAll('mst_in_box', where)
        return inboxDatas

    def getInboxData(self, where):
        inboxData = DaoBase().fetchOne('mst_in_box', where)
        return inboxData

    def getInboxesByCustomerId(self, id):
        inboxDatas = DaoBase().fetchAll('mst_in_box', {'customer_id': id})
        return inboxDatas


    def addInbox(self, datas):

        tableName = 'mst_in_box'
        result = DaoBase().insertRecord(tableName, datas)
        return result

    def getInboxDataWithEdit(self, id):
        inboxData = DaoBase().fetchOne('mst_in_box', id)
        return inboxData

    def saveInboxData(self, id, data):
        result = DaoBase().updateRecord('mst_in_box', data, id)
        return result