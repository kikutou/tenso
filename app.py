# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/model')
from flask import Flask, flash, render_template, request, json, redirect, session, url_for
from flaskext.mysql import MySQL
import datetime
import urllib
from bs4 import BeautifulSoup
import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#model add
from InboxModel import Inbox
from OutboxModel import Outbox
from UserAuthModel import User
from CustomerModel import Customer
from MadeInInfoModel import MadeInInfo
from RelInItemModel import RelInItem
from RelOutItemModel import RelOutItem

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'super secret key'



@app.before_request
def before_request():
    # session check
    if session.get('staff_name') is not None:
        return
    elif request.path == '/showLogin':
        return
    elif request.path == '/logout':
        return
    # ログインされておらずログインページに関するリクエストでもなければリダイレクトする
    else:
	if request.endpoint not in ('login', 'static'):
             return redirect('/showLogin')

@app.route("/")
def first():
    return redirect("/main")

@app.route("/main")
def main():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template("home.html", title="home")

@app.route('/logout', methods=['GET', 'POST'])
def showSignUp():
    if request.method == 'POST':
        user = User()
        newStaffData = {
            'name' : request.form['inputName'],
            'email' : request.form['inputEmail'],
            'password' : request.form['inputPassword']
        }
        result = user.do_register(newStaffData)
        if result:
            return render_template('login.html')
        else:
            return render_template('logout.html')
    else:
        return render_template('logout.html')


@app.route('/showLogin', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'POST':

        email = request.form['inputEmail']
        password = request.form['inputPassword']
        me = User(email)
        if me.check_password(password) and me.staff_name is not None:
            session['staff_name'] = me.staff_name
            session['id'] = me.staff_id
            return redirect("home")
        else:
            return "authentication failed"

    else:
        return render_template('login.html')

@app.route('/inboxCustomerSelect')
def inboxCustomerSelect():

    customers = Customer(app).getCustomers()

    return render_template('inboxCustomerSelect.html', title = unicode("入库箱信息-顾客选择", 'utf-8'), data=customers)


@app.route('/inboxIndex')
def inboxIndex():

    id = request.args.get('id')
    customer = Customer(app).getCustomer(int(id))

    inboxData = Inbox(app).getInboxesByCustomerId(int(id))

    inboxData = {key:record for key,record in inboxData.iteritems() if record['status'] == 0 or record['status'] == 1}

    return render_template('inboxIndex.html', title = unicode("入库箱信息", 'utf-8'), customer=customer, inboxData=inboxData)


@app.route('/inboxAdd', methods=['GET', 'POST'])
def inboxAdd():

    error = None
    if request.method == 'POST':

        customer_id = request.form['customer_id']
        staff_id = session.get('staff_id')
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': 0
                 }

        result = Inbox(app).addInbox(data)
        if result:
            flash('入库箱添加成功')
            return redirect('/inboxIndex?id=' + customer_id)
        else:
            error='入库箱添加失败'
    else:

        customerId = request.args.get('customerId')
        return render_template('inboxAdd.html', title=unicode('入库箱追加', 'utf-8'), customerId = customerId, error= error)

@app.route('/inboxEdit', methods=['GET', 'POST'])
def inboxEdit():

    error = None
    if request.method == 'POST':



        inboxId = request.form['id']

        customer_id = request.form['customer_id']
        staff_id = session.get('staff_id')
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': 0
                 }

        result = Inbox(app).saveInboxData(int(inboxId),data)
        if result:
            flash('入库箱更新成功')
            return redirect('/inboxIndex?id=' + customer_id)
        else:
            error='入库箱更新失败'
    else:

        inboxId = request.args.get('id')

    inboxData = Inbox(app).getInboxData(int(inboxId))

    return render_template('inboxAdd.html', title=unicode('入库箱追加', 'utf-8'), customerId = inboxData['customer_id'], inboxId = inboxId, inbox = inboxData, error= error)

@app.route('/inboxDelete', methods=['GET', 'POST'])
def inboxDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']
        customerId = request.form['customer_id']

        data = {
            'delete_flag': 1
        }

        result = Inbox(app).saveInboxData(int(id), data)
        if result:
            flash(unicode('入库箱删除成功', 'utf-8'))
            return redirect("inboxIndex?id=" + customerId)
        else:
            error = unicode('入库箱删除失败', 'utf-8')

    else:

        id = request.args.get('id')
        customerId = request.args.get('customer_id')

    return render_template('inboxDelete.html', title = unicode("确定删除", 'utf-8'), id = id,customer_id = customerId, error = error)




@app.route('/outboxCustomerSelect')
def outboxCustomerSelect():

    customers = Customer(app).getCustomers()

    return render_template('outboxCustomerSelect.html', title = unicode("出库箱信息-顾客选择", 'utf-8'), data=customers)


@app.route('/outboxInboxSelect')
def outboxInboxSelect():

    customerId = request.args.get('id')

    customer = Customer(app).getCustomer(int(customerId))

    inboxData = Inbox(app).getInboxesByCustomerId(int(customerId))

    inboxData = {key:record for key,record in inboxData.iteritems() if record['status'] == 0 or record['status'] == 1}

    return render_template('outboxInboxSelect.html', title = unicode("选择入库箱", 'utf-8'), customer=customer, inboxData=inboxData)


@app.route('/outboxInboxSelectConfirm', methods=['GET', 'POST'])
def outboxInboxSelectConfirm():

    if request.method == 'POST':
        inboxId = request.form['inbox_id']
        customerId = request.form['customer_id']

        data = {
            'status': 1
        }

        result = Inbox(app).saveInboxData(int(inboxId),data)
        if result:
            return redirect("outboxIndex?id=" + inboxId+'&customer_id=' + customerId)
        else:
            error = '入库箱选择失败'


    else:

        inboxId = request.args.get('id')
        customerId = request.args.get('customer_id')

    customer = Customer(app).getCustomer(int(customerId))

    inboxData = Inbox(app).getInboxData(int(inboxId))

    if inboxData['status'] == 1:
        return redirect("outboxIndex?customer_id=" + customerId)

    return render_template('outboxInboxSelectConfirm.html', title = unicode("入库箱选择确认", 'utf-8'), customer=customer, inboxData=inboxData)

@app.route('/outboxIndex')
def outboxIndex():

    customerId = request.args.get('customer_id')

    customer = Customer(app).getCustomer(int(customerId))

    inboxArray = Inbox(app).getInboxDatas({'status':1})

    outboxData = Outbox(app).getOutboxesByCustomerId(int(customerId))
    outboxData = {key:record for key,record in outboxData.iteritems() if record['status'] == 0 or record['status'] == 1}

    return render_template('outboxIndex.html', title = unicode("出库箱信息", 'utf-8'), customer=customer, inboxArray=inboxArray,outboxData = outboxData)

@app.route('/outboxAdd', methods=['GET', 'POST'])
def outboxAdd():
    error = None
    if request.method == 'POST':

        customer_id = request.form['customer_id']
        staff_id = session.get('staff_id')
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']

        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': 0,
                'update_at':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'update_by': staff_id
                 }

        result = Outbox(app).addOutbox(data)
        if result:
            flash('出库箱添加成功')
            return redirect('/outboxIndex?customer_id=' + customer_id)
        else:
            error='出库箱添加失败'
    else:

        customerId = request.args.get('customer_id')
        return render_template('outboxAdd.html', title=unicode('出库箱追加', 'utf-8'), customerId = customerId, error= error)





@app.route('/customer')
def customer():

    customers = Customer(app).getCustomers()

    return render_template('customer.html', title = unicode("顾客信息", 'utf-8'),customersData = customers)

@app.route('/customerAdd', methods=['GET', 'POST'])
def customerAdd():

    error = None

    if request.method == 'POST':

        name = request.form['name']
        real_name = request.form['real_name']
        address = request.form['address']
        telephone1 = request.form['telephone1']
        telephone2 = request.form['telephone2']
        email = request.form['email']
        company_name = request.form['company_name']
        company_address = request.form['company_address']
        company_telephone = request.form['company_telephone']
        if request.form['id_confirmed_flag']:
            id_confirmed_flag = 1
        else:
            id_confirmed_flag = 0

        if request.form['id_card_no']:
            id_card_no = request.form['id_card_no']
        else:
            id_card_no = null

        data = {
            'name': name,
            'real_name': real_name,
            'address': address,
            'telephone1': telephone1,
            'telephone2': telephone2,
            'email': email,
            'company_name': company_name,
            'company_address': company_address,
            'company_telephone': company_telephone,
            'id_confirmed_flag': id_confirmed_flag,
            'id_card_no': id_card_no,
        }

        result = Customer(app).insertCustomer(data)

        if result:
            flash(unicode('顾客添加成功', 'utf-8'))
            return redirect("customer")
        else:
            error = unicode('顾客添加失败', 'utf-8')


    return render_template('customerAdd.html', title = unicode("顾客信息", 'utf-8'), error = error)

@app.route('/customerEdit', methods=['GET', 'POST'])
def customerEdit():

    error = None

    if request.method == 'POST':

        id = request.form['id']

        name = request.form['name']
        real_name = request.form['real_name']
        address = request.form['address']
        telephone1 = request.form['telephone1']
        telephone2 = request.form['telephone2']
        email = request.form['email']
        company_name = request.form['company_name']
        company_address = request.form['company_address']
        company_telephone = request.form['company_telephone']
        if request.form['id_confirmed_flag']:
            id_confirmed_flag = 1
        else:
            id_confirmed_flag = 0
        id_card_no = request.form['id_card_no']

        data = {
            'name': name,
            'real_name': real_name,
            'address': address,
            'telephone1': telephone1,
            'telephone2': telephone2,
            'email': email,
            'company_name': company_name,
            'company_address': company_address,
            'company_telephone': company_telephone,
            'id_confirmed_flag': id_confirmed_flag,
            'id_card_no': id_card_no,
        }

        result = Customer(app).updateCustomer(data,int(id))

        if result:
            flash(unicode('顾客编辑成功', 'utf-8'))
            return redirect("customer")
        else:
            error = unicode('顾客编辑失败', 'utf-8')

    else:
        id = request.args.get('id')

    customer = Customer(app).getCustomer(int(id))

    return render_template('customerAdd.html', title = unicode("顾客信息", 'utf-8'),data = customer, error = error)


@app.route('/customerDelete', methods=['GET', 'POST'])
def customerDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Customer(app).updateCustomer(data,int(id))
        if result:
            flash(unicode('顾客删除成功', 'utf-8'))
            return redirect("customer")
        else:
            error = unicode('顾客删除失败', 'utf-8')

    else:

        id = request.args.get('id')

    return render_template('customerDelete.html', title = unicode("确定删除", 'utf-8'), id = id, error = error)


@app.route('/itemAdd', methods=['GET', 'POST'])
def itemAdd():

    jancode = request.args.get('jancode')

    try:
        html = urllib.urlopen('http://www.janken.jp/goods/jk_catalog_syosai.php?jan=' + jancode)
    except Error as e:
        print e

    soup = BeautifulSoup(html.read(),"html.parser")

    itemTable = soup.select('table[summary="登録情報"]')[0]

    itemNameJp = itemTable.find_all('tr')[0].find_all('td')[1].h5.string

    price = itemTable.find_all('tr')[13].find_all('td')[1].string

    if price:
        price = price[1:]

    memo = itemTable.find_all('tr')[14].find_all('td')[1].string



    madeInInfos = MadeInInfo(app).getMadeInInfos()



    return render_template('itemAdd.html', title = unicode("商品添加", 'utf-8'),jancode=jancode, itemNameJp = itemNameJp,
                           price = price, memo = memo, madeInInfos = madeInInfos, )





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
