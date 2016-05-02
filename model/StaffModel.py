import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../dao')
from time import gmtime, strftime
#dao add
from DaoBaseDBAccess import DaoBase

class Staff(object):

    def __init__(self, app):
        pass

    def getStaff(self, id):
        staffRecord = DaoBase().fetchOne('mst_staff', id)
        return staffRecord

    def getStaffs(self):
        staffRecords = DaoBase().fetchAll('mst_staff')
        return staffRecords

    def insertStaff(self,data):
        result = DaoBase().insertRecord('mst_staff',data)
        return result

    def updateStaff(self, id, data):
        result = DaoBase().updateRecord('mst_staff',data,id)
        return result
