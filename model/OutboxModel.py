# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime

#dao add
from DaoBaseDBAccess import DaoBase

class Outbox():

    def __init__(self, app):
        pass


    def getCustomer(self, id):
        customerRecord = DaoBase().fetchOne('mst_customer', id)
        return customerRecord

    def getOutboxDatas(self,where):
        outboxDatas = DaoBase().fetchAll('mst_out_box',where)
        return outboxDatas

    def getOutboxesByCustomerId(self, id):
        outboxDatas = DaoBase().fetchAll('mst_out_box', {'customer_id': id})
        return outboxDatas

    def getOutboxData(self, where):
        outboxData = DaoBase().fetchOne('mst_out_box', where)
        return outboxData

    def addOutbox(self, datas):
        tableName = 'mst_out_box'
        result = DaoBase().insertRecord(tableName, datas)
        return result

    def getOutboxDataWithEdit(self, id):
        inboxData = DaoBase().fetchOne('mst_out_box', id)
        return inboxData

    def saveOutboxData(self, id, datas):
        result = DaoBase().updateRecord('mst_out_box', datas, id)
        return result

    def getOutboxDataBySearch(self, where):

        result = DaoBase().fetchAllBySearch('mst_out_box', where)
        return result