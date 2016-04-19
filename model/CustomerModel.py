import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime
#dao add
from DaoBaseDBAccess import DaoBase

class Customer(object):

    def __init__(self, app):
        pass

    def getCustomer(self, id):
        customerRecord = DaoBase().fetchOne('mst_customer', id)
        return customerRecord

    def getCustomers(self):
        customerRecords = DaoBase().fetchAll('mst_customer')
        return customerRecords

    def insertCustomer(self,data):
        result = DaoBase().insertRecord('mst_customer',data)
        return result

    def updateCustomer(self, data, id):
        result = DaoBase().updateRecord('mst_customer',data,id)
        return result
