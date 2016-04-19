# -*- coding: utf-8 -*-
from flaskext.mysql import MySQL
from flask import Flask
app = Flask(__name__)

class DaoBase(object):

    def __init__(self):
        # MySQL configurations
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
        app.config['MYSQL_DATABASE_DB'] = 'qh_logistics'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
        self.conn = mysql.connect()


    def insertRecord(self, tableName, datas):
        # datas is a hash map with
        # the key for the column name and the value for the column value
        if tableName is None:
            return 0
        if datas is None:
            return 0
        if not isinstance(datas, dict):
            # hash map check
            return 0

        keys = "`DELETE_FLAG`, "
        values = "0, "
        for key, value in datas.items():

             keys += "`"+key+"`, "

             if isinstance(value, str) or isinstance(value, unicode):
                 values += "'" + value + "', "
             else:
                 values += "'" + str(value) + "', "

        keys = keys[:-2] + ") "
        values = values[:-2] + ");"

        insertString = "INSERT INTO `qh_logistics`.`" + str(tableName) + "` (" + keys + "VALUES (" + values
        result = self.conn.cursor().execute(insertString)

        if result is None:
            return 0
        else:
            self.conn.commit()
            self.conn.close()
            return result


    def updateRecord(self, tableName, datas, where):
        # datas [where] is a hash map with
        # the key for the column name and the value for the column value
        # when [where] is a Int also can through this method

        updateString = "UPDATE `qh_logistics`.`" + tableName + "` SET "
        if tableName is None:
            return 0
        if datas is None:
            return 0
        if not isinstance(datas, dict):
            return 0
        if where is None:
            return 0
        else:
            values = ""
            for key, value in datas.items():

                if isinstance(value, str) or isinstance(value, unicode):
                    values += "`" + key + "`='" + value + "', "
                else:
                    values += "`" + key + "`='" + str(value) + "', "

            updateString += values[:-2]

            if isinstance(where, int):

                updateString += " WHERE `id`=" + str(where) + ";"

            elif isinstance(where, dict):

                for key, value in where.items():

                    if isinstance(value, str) or isinstance(value, unicode):
                        values += "`" + key + "`='" + value + "' "
                    else:
                        values += "`" + key + "`='" + str(value) + "' "

                updateString += " WHERE " + values + ";"

        result = self.conn.cursor().execute(updateString)

        if result is None:
            return 0
        else:
            self.conn.commit()
            self.conn.close()
            return result


    def fetchOne(self, tableName, where=None):

        cursor = self.doSelect(tableName, where)
        result = self.fetchOneAssoc(cursor)
        self.conn.close()

        if result is None:
            return 0
        else:
            return result


    def fetchAll(self, tableName, where=None):

        cursor = self.doSelect(tableName, where)
        result = self.fetchAllAssoc(cursor)
        self.conn.close()

        if result is None:
            return 0
        else:
            return result


    def doSelect(self, tableName, where):
        # (where) is a id or hash map
        # hash map with
        # the key for the column name the value for the column value
        if tableName is None:
            return 0

        if where is None:

            selectString = "SELECT * FROM " + str(tableName) + " WHERE DELETE_FLAG = 0;"

        else:

            if isinstance(where, int):

                selectString = "SELECT * FROM " + str(tableName) + " WHERE DELETE_FLAG = 0 AND id = " + str(where) + ";"

            elif isinstance(where, dict):

                newWhere = ""
                for key, value in where.items():
                    if isinstance(value, str) or isinstance(value, unicode):
                        newWhere += newWhere + key + " = '" + value + "'"
                    else:
                        newWhere += newWhere + key + " = '" + str(value) + "'"

                selectString = "SELECT * FROM " + str(tableName) + " WHERE DELETE_FLAG = 0 AND " + newWhere + ";"

            else:
                return 0

        cursor = self.conn.cursor()
        cursor.execute(selectString)
        return cursor

    def fetchOneAssoc(self,cursor):

        data = cursor.fetchone()
        if data == None:
            return None
        desc = cursor.description

        dict = {}
        for (name, value) in zip(desc, data):
            dict[name[0]] = value

        return dict

    def fetchAllAssoc(self, cursor):

        datas = cursor.fetchall()
        if datas == None:
            return None

        desc = cursor.description
        dicts = {}
        idx = 0
        for data in datas:
            dict = {}
            for (name, value) in zip(desc, data):
                dict[name[0]] = value

            dicts[idx] = dict
            idx += 1
        return dicts

