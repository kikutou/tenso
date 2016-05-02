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
from ItemModel import Item
from UserAuthModel import User
from CustomerModel import Customer
from MadeInInfoModel import MadeInInfo
from RelInItemModel import RelInItem
from RelOutItemModel import RelOutItem
from StaffModel import Staff

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
        pass
        # user = User()
        # newStaffData = {
        #     'name' : request.form['inputName'],
        #     'email' : request.form['inputEmail'],
        #     'password' : request.form['inputPassword']
        # }
        # result = user.do_register(newStaffData)
        # if result:
        #     return render_template('login.html')
        # else:
        #     return render_template('logout.html')
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
            session['staff_id'] = me.staff_id
            session['auth'] = me.authority
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


@app.route('/outboxEdit', methods=['GET', 'POST'])
def outboxEdit():

    error = None
    if request.method == 'POST':



        outboxId = request.form['id']

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

        result = Outbox(app).saveOutboxData(data, int(outboxId))
        if result:
            flash('出库箱更新成功')
            return redirect('/outboxIndex?id=' + customer_id)
        else:
            error='出库箱更新失败'
    else:

        outboxId = request.args.get('id')

    outboxData = Outbox(app).getOutboxData(int(outboxId))

    return render_template('outboxAdd.html', title=unicode('出库箱追加', 'utf-8'), customerId = outboxData['customer_id'], outboxId = outboxId, outbox = outboxData, error= error)


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

    error = None

    if request.method == 'POST':



        '''
        手順：
        ①DBに商品情報を書き込む
        DBから試して、商品情報を取得する。
            あれば、更新
            なければ、追加

        ②DBに商品と入庫箱の関係テーブルを書き込む
        DBから、入庫箱IDと商品IDをセットにして、試して関係を取得する
            あれば、数目を更新する
            なければ、追加

        ③DBに商品と出庫箱の関係テーブルを書き込む
        DBから、出庫箱IDと商品IDをセットにして、試して関係を取得する
            あれば、数目を更新する
            なければ、追加
        '''
        #①DBに商品情報を書き込む
        #janコードを取得する。
        jancode = request.form['jan_code']

        #DBから商品情報を試して取得する。
        item = Item(app).getItem({'jan_code': jancode})

        data = {
                'jan_code': jancode,
                'jp_name': request.form['jp_name'],
                'en_name': request.form['en_name'],
                'cn_name': request.form['cn_name'],
                'unit_price': request.form['unit_price'],
                'memo': request.form['memo'],
                'country_of_origin': request.form['country_of_origin']
            }

        if item:

            itemId = item['id']

            #あれば、更新
            result = Item(app).saveItem(itemId, data)

        else:
            #なければ、追加
            result = Item(app).addItem(data)
            if not result:
                error = unicode('商品添加失败', 'utf-8')


        #②DBに商品と入庫箱の関係テーブルを書き込む

        #DBから商品情報を試して取得する。
        item = Item(app).getItem({'jan_code': jancode})
        itemId = item['id']

        inboxId = request.form['inbox']
        itemNum = request.form['number']
        checkTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        relInItem = RelInItem(app).getRelInItem({'in_box_id': inboxId,'item_id':itemId})

        if relInItem:
            relInItemId = relInItem['id']

            data = {
                'check_time': checkTime,
                'in_box_id': inboxId,
                'item_id': itemId,
                'item_num': int(itemNum) + int(relInItem['item_num'])
            }

            result = RelInItem(app).saveRelInItem(int(relInItemId),data)
            if not result:
                error = unicode('商品添加失败', 'utf-8')
        else:

            data = {
                'check_time': checkTime,
                'in_box_id': inboxId,
                'item_id': itemId,
                'item_num': int(itemNum)
            }

            result = RelInItem(app).addRelInItem(data)
            if not result:
                error = unicode('商品添加失败', 'utf-8')


        #②DBに商品と出庫箱の関係テーブルを書き込む
        outboxId = request.form['outbox']

        relOutItem = RelOutItem(app).getRelOutItem({'out_box_id': outboxId,'item_id':itemId})

        if relOutItem:
            relOutItemId = relOutItem['id']

            data = {
                'check_time': checkTime,
                'out_box_id': outboxId,
                'item_id': itemId,
                'item_num': int(itemNum) + int(relOutItem['item_num'])
            }

            result = RelOutItem(app).saveRelOutItem(int(relOutItemId),data)
            if not result:
                error = unicode('商品添加失败', 'utf-8')
        else:

            data = {
                'check_time': checkTime,
                'out_box_id': outboxId,
                'item_id': itemId,
                'item_num': int(itemNum)
            }

            result = RelOutItem(app).addRelOutItem(data)
            if not result:
                error = unicode('商品添加失败', 'utf-8')

        if not error:
            flash(unicode('顾客删除成功', 'utf-8'))
            return redirect("itemAddSuccess")




    else:

        '''
        手順
         ①スマホで、アプリを使って、商品のJANコードを取得する。
         ②DBから商品情報を試して取得する。
            取得できれば、DBのテーブルの該当情報をページ上に表示する。
            取得できなければ、ウェブサイトから、商品情報を取得する。

        産地、入庫箱と出庫箱をDBから取得する

        ③取得された商品情報を手動で、補足する。
        ④入庫箱を選び
        ⑤出庫箱を選び
        ⑥情報をDBに反映する。
        '''

        #janコードを取得する。
        jancode = request.args.get('jancode')

        #DBから商品情報を試して取得する。
        item = Item(app).getItem({'jan_code': jancode})

        if not item:
            #取得できなければ、ウェブサイトから、商品情報を取得する。
            try:
                html = urllib.urlopen('http://www.janken.jp/goods/jk_catalog_syosai.php?jan=' + jancode)
            except Error as e:
                print e

            soup = BeautifulSoup(html.read(),"html.parser")

            itemTable = soup.select('table[summary="登録情報"]')[0]
            #商品の日本語名前
            itemNameJp = itemTable.find_all('tr')[0].find_all('td')[1].h5.string
            #商品の参照単価
            price = itemTable.find_all('tr')[13].find_all('td')[1].string

            if price:
                price = price[1:]
            #商品の備考（分類）
            memo = itemTable.find_all('tr')[14].find_all('td')[1].string

            item = {
                'jan_code': jancode,
                'jp_name': itemNameJp,
                'unit_price': price,
                'memo': memo
            }

    madeInInfos = MadeInInfo(app).getMadeInInfos(None)
    inboxes = Inbox(app).getInboxDatas({'status': 1, 'staff_id':session.get('staff_id')})
    outboxes = Outbox(app).getOutboxDatas({'status': 0, 'staff_id':session.get('staff_id')})


    return render_template('itemAdd.html', title = unicode("商品添加", 'utf-8'),item = item, madeInInfos = madeInInfos,
                           inboxes = inboxes, outboxes = outboxes ,error = error)


@app.route('/itemAddSuccess', methods=['GET', 'POST'])
def itemAddSuccess():

    error = None

    if request.method == 'POST':
        inboxId = request.form['inbox_id']
        outboxId = request.form['outbox_id']

        if inboxId and not outboxId:
            Inbox(app).saveInboxData(int(inboxId),{'status': 2})
        elif not inboxId and outboxId:
            Outbox(app).saveOutboxData(int(outboxId),{'status': 1})
        else:
            error = '未知错误'


    inboxes = Inbox(app).getInboxDatas({'status': 1, 'staff_id': session.get('staff_id')})

    if inboxes:
        inbox = inboxes[0]
        customerId = inbox['customer_id']
        customer = Customer(app).getCustomer(int(customerId))
        if not customer:
            error = '没有找到相应的顾客信息'

    outboxes = Outbox(app).getOutboxDatas({'status': 0, 'staff_id': session.get('staff_id')})

    return render_template('itemAddSuccess.html', title = unicode("货物添加成功", 'utf-8'), error = error, inboxes = inboxes,
                           customer = customer, outboxes = outboxes)


@app.route('/outboxInfo', methods=['GET', 'POST'])
def outboxInfo():

    error = None

    outboxId = request.args.get('id')

    outbox = Outbox(app).getOutboxData(int(outboxId))

    customerId = outbox['customer_id']

    customer = Customer(app).getCustomer(int(customerId))

    relOutItems = RelOutItem(app).getRelOutItems({'out_box_id': outboxId})

    items = []

    for key,relOutItem in relOutItems.items():
        itemId = relOutItem['item_id']
        itemNum = relOutItem['item_num']

        item = Item(app).getItem(int(itemId))
        itemNameJp = item['jp_name']
        itemNameEn = item['en_name']
        itemNameCn = item['cn_name']
        itemPrice = item['unit_price']
        jancode = item['jan_code']

        data = {
            'id': itemId,
            'item_num': itemNum,
            'jp_name': itemNameJp,
            'en_name': itemNameEn,
            'cn_name': itemNameCn,
            'jan_code': jancode,
            'unit_price': itemPrice
        }

        items.append(data)


    return render_template('outboxInfo.html', title = unicode("出库箱详细", 'utf-8'), error = error, outbox = outbox,
                           customer = customer, items = items)


@app.route('/removeItem', methods=['GET', 'POST'])
def removeItem():

    error = None

    if request.method == 'POST':
        srcOutbox = request.form['src_outbox']
        desOutbox = request.form['des_outbox']
        itemId = request.form['item_id']
        num = request.form['number']

        '''
        ①移動する数目をチェックする
        ②元のoutboxから、数目を更新
            全部移動する場合、元のレコードを削除
            一部移動する場合、数目を更新する
        ③移動先のoutboxの数目を更新
            すでにある場合、数目を増加して、更新する
            なければ、新規追加

        '''
        #①移動する数目をチェックする
        relOutItem = RelOutItem(app).getRelOutItem({'out_box_id': srcOutbox, 'item_id': itemId})
        oldNum = relOutItem['item_num']
        if int(num) > int(oldNum):
            error = '移动数目不正确，请重新输入'

        if not error:
            #②元のoutboxから、数目を更新
            if int(num) == int(oldNum):
                RelOutItem(app).saveRelOutItem(int(relOutItem['id']),{'delete_flag': 1})
            else:
                leftNum = int(oldNum) - int(num)
                RelOutItem(app).saveRelOutItem(int(relOutItem['id']),{'item_num': leftNum})

            #移動先のoutboxの数目を更新
            desRelOutItem = RelOutItem(app).getRelOutItem({'out_box_id': desOutbox, 'item_id': itemId})
            if desRelOutItem:
                #すでにある場合、数目を増加して、更新する
                newNum = int(desRelOutItem['item_num']) + int(num)
                RelOutItem(app).saveRelOutItem(int(desRelOutItem['id']),{'item_num': newNum})
            else:
                data = {
                    'check_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'out_box_id': desOutbox,
                    'item_id': itemId,
                    'item_num': num
                }
                RelOutItem(app).addRelOutItem(data)

            flash('货物移动成功')

            return redirect('/outboxInfo?id=' + srcOutbox)

    customerId = request.args.get('customer_id')
    outboxId = request.args.get('outbox_id')
    itemId = request.args.get('item_id')

    customer = Customer(app).getCustomer(int(customerId))
    outbox = Outbox(app).getOutboxData(int(outboxId))
    item = Item(app).getItem(int(itemId))
    relOutItem = RelOutItem(app).getRelOutItems({'out_box_id': outboxId, 'item_id': item['id']})

    outboxes = Outbox(app).getOutboxDatas({'status': 0, 'staff_id': session.get('staff_id'), 'customer_id': customerId})


    return render_template('removeItem.html', title = unicode("出库箱详细", 'utf-8'), error = error, outbox = outbox,
                           customer = customer, item = item, relOutItem = relOutItem, outboxes = outboxes)


@app.route('/adminInbox', methods=['GET', 'POST'])
def adminInbox():

    error = None

    date_from = ''
    date_to = ''
    name = ''
    status = ''

    if request.method == 'POST':
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        name = request.form['name']
        status = request.form['status']

        where = {}
        if date_from:
            where['date_from'] = date_from + ' 00:00:00'
        if date_to:
            where['date_to'] = date_to + ' 23:59:59'
        if name:
            where['name'] = name
        if status:
            where['status'] = status

        if len(where) == 0:
            inboxData = Inbox(app).getInboxDataBySearch(None)
        else:
            inboxData = Inbox(app).getInboxDataBySearch(where)

    else:

        date_from = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        date_to = datetime.datetime.now().strftime("%Y-%m-%d 23:59:59")

        inboxData = Inbox(app).getInboxDataBySearch({'date_from':date_from, 'date_to':date_to})

    newInboxData = {}

    for key,record in inboxData.items():
        staffId = record['staff_id']
        staff = Staff(app).getStaff(int(staffId))
        if staff:
            record['staff_name'] = staff['name']
        else:
            record['staff_name'] = '未设定'

        newInboxData[key] = record




    return render_template('adminInboxList.html', title = unicode("入库箱管理", 'utf-8'), error = error,
                           inboxData = newInboxData, date_from = date_from[:10], date_to = date_to[:10], name = name, status = status)


@app.route('/adminInboxEdit', methods=['GET', 'POST'])
def adminInboxEdit():

    error = None
    if request.method == 'POST':

        inboxId = request.form['id']

        customer_id = request.form['customer_id']
        staff_id = request.form['staff_id']
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        status = request.form['status']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': status
                 }

        result = Inbox(app).saveInboxData(int(inboxId),data)
        if result:
            flash('入库箱更新成功')
            return redirect('/adminInbox')
        else:
            error='入库箱更新失败'
    else:

        inboxId = request.args.get('id')

    inboxData = Inbox(app).getInboxData(int(inboxId))
    customers = Customer(app).getCustomers()
    staffs = Staff(app).getStaffs()

    return render_template('adminInboxEdit.html', title=unicode('入库箱追加', 'utf-8'), customers = customers,
                           staffs = staffs, inbox = inboxData, error= error)

@app.route('/adminInboxAdd', methods=['GET', 'POST'])
def adminInboxAdd():

    error = None
    if request.method == 'POST':

        customer_id = request.form['customer_id']
        staff_id = request.form['staff_id']
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        status = request.form['status']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': status
        }

        result = Inbox(app).addInbox(data)
        if result:
            flash('入库箱更新成功')
            return redirect('/adminInbox')
        else:
            error='入库箱更新失败'

    customers = Customer(app).getCustomers()
    staffs = Staff(app).getStaffs()

    return render_template('adminInboxAdd.html', title=unicode('入库箱追加', 'utf-8'), customers = customers,
                           staffs = staffs, error= error)

@app.route('/adminInboxDelete', methods=['GET', 'POST'])
def adminInboxDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Inbox(app).saveInboxData(int(id), data)
        if result:
            flash(unicode('入库箱删除成功', 'utf-8'))
            return redirect("adminInbox")
        else:
            error = unicode('入库箱删除失败', 'utf-8')

    else:

        id = request.args.get('id')

    return render_template('adminInboxDelete.html', title = unicode("确定删除", 'utf-8'), id = id, error = error)


@app.route('/adminOutbox', methods=['GET', 'POST'])
def adminOutbox():

    error = None

    date_from = ''
    date_to = ''
    name = ''
    status = ''

    if request.method == 'POST':
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        name = request.form['name']
        status = request.form['status']

        where = {}
        if date_from:
            where['date_from'] = date_from + ' 00:00:00'
        if date_to:
            where['date_to'] = date_to + ' 23:59:59'
        if name:
            where['name'] = name
        if status:
            where['status'] = status

        if len(where) == 0:
            outboxData = Outbox(app).getOutboxDataBySearch(None)
        else:
            outboxData = Outbox(app).getOutboxDataBySearch(where)

    else:

        date_from = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        date_to = datetime.datetime.now().strftime("%Y-%m-%d 23:59:59")

        outboxData = Outbox(app).getOutboxDataBySearch(None)

    newOutboxData = {}

    for key,record in outboxData.items():
        staffId = record['staff_id']
        staffName = Staff(app).getStaff(int(staffId))['name']
        record['staff_name'] = staffName
        newOutboxData[key] = record


    return render_template('adminOutboxList.html', title = unicode("出库箱管理", 'utf-8'), error = error,
                           outboxData = newOutboxData, date_from = date_from[:10], date_to = date_to[:10], name = name, status = status)

@app.route('/adminOutboxEdit', methods=['GET', 'POST'])
def adminOutboxEdit():

    error = None
    if request.method == 'POST':

        outboxId = request.form['id']

        customer_id = request.form['customer_id']
        staff_id = request.form['staff_id']
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        status = request.form['status']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': status
                 }

        result = Outbox(app).saveOutboxData(int(outboxId),data)
        if result:
            flash('出库箱更新成功')
            return redirect('/adminOutbox')
        else:
            error='出库箱更新失败'
    else:

        outboxId = request.args.get('id')

    outboxData = Outbox(app).getOutboxData(int(outboxId))
    customers = Customer(app).getCustomers()
    staffs = Staff(app).getStaffs()

    return render_template('adminOutboxEdit.html', title=unicode('出库箱追加', 'utf-8'), customers = customers,
                           staffs = staffs, outbox = outboxData, error= error)

@app.route('/adminOutboxAdd', methods=['GET', 'POST'])
def adminOutboxAdd():

    error = None
    if request.method == 'POST':

        customer_id = request.form['customer_id']
        staff_id = request.form['staff_id']
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        status = request.form['status']
        data = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight,
                'customer_id': customer_id,
                'staff_id': staff_id,
                'status': status
        }

        result = Outbox(app).addOutbox(data)
        if result:
            flash('出库箱更新成功')
            return redirect('/adminOutbox')
        else:
            error='出库箱更新失败'

    customers = Customer(app).getCustomers()
    staffs = Staff(app).getStaffs()

    return render_template('adminOutboxAdd.html', title=unicode('出库箱追加', 'utf-8'), customers = customers,
                           staffs = staffs, error= error)

@app.route('/adminOutboxDelete', methods=['GET', 'POST'])
def adminOutboxDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Outbox(app).saveOutboxData(int(id), data)
        if result:
            flash(unicode('出库箱删除成功', 'utf-8'))
            return redirect("adminOutbox")
        else:
            error = unicode('出库箱删除失败', 'utf-8')

    else:

        id = request.args.get('id')

    return render_template('adminOutboxDelete.html', title = unicode("确定删除", 'utf-8'), id = id, error = error)

@app.route('/adminCustomer', methods=['GET', 'POST'])
def adminCustomer():

    error = None


    customer = Customer(app).getCustomers()
    if customer == 0:
        error = "can not found the customer datas!"

    return render_template('adminCustomerList.html', title = unicode("客户管理", 'utf-8'), error = error, viewCustomer = customer)


@app.route('/adminCustomerAdd', methods=['GET', 'POST'])
def adminCustomerAdd():

    error = None
    if request.method == 'POST':

        name = request.form['name']
        real_name = request.form['real_name']
        address = request.form['address']
        telephone1 = request.form['telephone1']
        telephone2 = request.form['telephone2']
        email = request.form['email']
        id_card_no = request.form['id_card_no']
        company_name = request.form['company_name']
        company_address = request.form['company_address']
        company_telephone = request.form['company_telephone']
        data = {'name' : name,
                 'real_name' : real_name,
                 'address' : address,
                 'telephone1' : telephone1,
                 'telephone2' : telephone2,
                 'email' : email,
                'id_card_no': id_card_no,
                'company_name': company_name,
                'company_address': company_address,
                'company_telephone': company_telephone
        }

        result = Customer(app).insertCustomer(data)
        if result:
            flash('顾客信息更新成功')
            return redirect('/adminCustomer')
        else:
            error='顾客信息更新失败'

    customers = Customer(app).getCustomers()
    staffs = Staff(app).getStaffs()

    return render_template('adminCustomerAdd.html', title=unicode('顾客信息追加', 'utf-8'), customers = customers,
                           staffs = staffs, error= error)

@app.route('/adminCustomerEdit', methods=['GET', 'POST'])
def adminCustomerEdit():

    error = None
    if request.method == 'POST':

        customer = request.form['id']

        name = request.form['name']
        real_name = request.form['real_name']
        address = request.form['address']
        telephone1 = request.form['telephone1']
        telephone2 = request.form['telephone2']
        email = request.form['email']
        id_card_no = request.form['id_card_no']
        company_name = request.form['company_name']
        company_address = request.form['company_address']
        company_telephone = request.form['company_telephone']
        data = {'name' : name,
                 'real_name' : real_name,
                 'address' : address,
                 'telephone1' : telephone1,
                 'telephone2' : telephone2,
                 'email' : email,
                'id_card_no': id_card_no,
                'company_name': company_name,
                'company_address': company_address,
                'company_telephone': company_telephone
                 }

        result = Customer(app).updateCustomer(data, int(customer))
        if result:
            flash('顾客信息更新成功')
            return redirect('/adminCustomer')
        else:
            error='顾客信息更新失败'
    else:

        customer_id = request.args.get('id')


        customer = Customer(app).getCustomer(int(customer_id))


    return render_template('adminCustomerEdit.html', title = unicode('顾客信息编辑', 'utf-8'), customer = customer,
                           error = error)

@app.route('/adminCustomerDelete', methods=['GET', 'POST'])
def adminCustomerDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Customer(app).updateCustomer(data, int(id))
        if result:
            flash(unicode('顾客信息删除成功', 'utf-8'))
            return redirect("adminCustomer")
        else:
            error = unicode('顾客信息删除失败', 'utf-8')

    else:

        id = request.args.get('id')

    return render_template('adminCustomerDelete.html', title = unicode("确定删除", 'utf-8'), id = id, error = error)

@app.route('/adminStaff', methods=['GET', 'POST'])
def adminStaff():

    error = None


    customer = Staff(app).getStaffs()
    if customer == 0:
        error = "can not found the customer datas!"

    return render_template('adminStaffList.html', title = unicode("客户管理", 'utf-8'), error = error, viewStaff = customer)

@app.route('/adminStaffAdd', methods=['GET', 'POST'])
def adminStaffAdd():

    error = None
    if request.method == 'POST':
        user = User()

        staff_cd = request.form['staff_cd']
        name = request.form['name']
        telphone = request.form['telphone']
        email = request.form['email']
        password = request.form['password']

        data = {'staff_cd': staff_cd,
                'name' : name,
                'telphone' : telphone,
                'email': email,
                'password': password

        }

        #result = Staff(app).insertStaff(data)
        result = user.do_register(data)
        if result:
            flash('职员信息更新成功')
            return redirect('/adminStaff')
        else:
            error='职员信息更新失败'

    staffs = Staff(app).getStaffs()

    return render_template('adminStaffAdd.html', title=unicode('职员信息追加', 'utf-8'), staffs = staffs, error= error)

@app.route('/adminStaffEdit', methods=['GET', 'POST'])
def adminStaffEdit():

    error = None

    if request.method == 'POST':
        user = User()

        id = request.form['id']
        staff_cd = request.form['staff_cd']
        name = request.form['name']
        telphone = request.form['telphone']
        email = request.form['email']
        password = request.form['password']

        data = {'staff_cd': staff_cd,
                'name' : name,
                'telphone' : telphone,
                'email': email,
                'password': password

        }

        result = user.update_staff(data, int(id))
        if result:
            flash('职员信息更新成功')
            return redirect('/adminStaff')
        else:
            error='职员信息更新失败'

    else:

        staffId = request.args.get('id')


        staff = Staff(app).getStaff(int(staffId))


    return render_template('adminStaffEdit.html', title = unicode('职员信息编辑', 'utf-8'), staff = staff,
                           error = error)

@app.route('/adminStaffDelete', methods=['GET', 'POST'])
def adminStaffDelete():

    error = None

    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Staff(app).updateStaff(int(id), data)
        if result:
            flash(unicode('职员信息删除成功', 'utf-8'))
            return redirect("adminStaff")
        else:
            error = unicode('职员信息删除失败', 'utf-8')

    else:

        id = request.args.get('id')

    return render_template('adminStaffDelete.html', title = unicode("确定删除", 'utf-8'), id = id, error = error)

@app.route("/adminHome")
def adminHome():
    if session['auth'] == 1:
        return render_template("adminHome.html", title="adminHome")
    else:
        return render_template("home.html", title="home")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
