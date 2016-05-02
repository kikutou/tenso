# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, \
    check_password_hash

#dao add
from DaoBaseDBAccess import DaoBase
class User(object):
    def __init__(self, email=None):
        self.staff_name = None
        self.pw_hash = ""
        if email is not None:
            staff_data = DaoBase().fetchOne('mst_staff', {'email': email})
            if staff_data:
                self.staff_id = staff_data['id']
                self.staff_name = staff_data['name']
                self.email = staff_data['email']
                self.pw_hash = staff_data['password']
                self.authority = staff_data['authority']


    def do_register(self, newStaffData):
        pw_hash = generate_password_hash(newStaffData['password'])
        newStaffData['password'] = pw_hash
        result = DaoBase().insertRecord('mst_staff', newStaffData)
        return result


    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def update_staff(self, editData, id):

        data = {'staff_cd': editData['staff_cd'],
                'name' : editData['name'],
                'telphone' : editData['telphone'],
                'email': editData['email'],
            }

        if editData['password'] != "":
            pw_hash = generate_password_hash(editData['password'])
            data['password'] = pw_hash

        result = DaoBase().updateRecord('mst_staff', data, id)
        return result
