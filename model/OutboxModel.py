# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class Outbox():


    def getCustomer(self, id):
        customerRecord = DaoBase().fetchOne('mst_customer', id)
        return customerRecord

    def getOutboxDatas(self):
        outboxDatas = DaoBase().fetchAll('mst_out_box')
        return outboxDatas

    def addOutbox(self, datas):

        tableName = 'mst_out_box'
        result = DaoBase().insertRecord(tableName, datas)
        return result

    def getOutboxDataWithEdit(self, id):
        inboxData = DaoBase().fetchOne('mst_out_box', id)
        return inboxData

    def saveInboxData(self, id, datas):
        result = DaoBase().updateRecord('mst_out_box', datas, id)
        return result
