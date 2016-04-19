# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/model')
from flask import Flask, render_template, request, json, redirect, session, url_for
from flaskext.mysql import MySQL


#model add
from InboxModel import Inbox
from UserAuthModel import User
from CustomerModel import Customer

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
            return redirect("home")
        else:
            return "authentication failed"

    else:
        return render_template('login.html')

# @app.route('/signUp', methods=['GET', 'POST'])
# def signUp():
#
#     # create user code will be here !!
#     _name = request.form['inputName']
#     _email = request.form['inputEmail']
#     _password = request.form['inputPassword']
#
#
#     _hashed_password = generate_password_hash(_password)
#     cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
#     data = cursor.fetchall()
#
#     # If the procedure is executed successfully,
#     # then we'll commit the changes and return the success message.
#     if len(data) is 0:
#         conn.commit()
#         return render_template("index.html")
#     else:
#         return json.dumps({'error':str(data[0])})

@app.route('/inboxIndex')
def inboxIndex():
    id = int("1") # get the customer id from url
    inbox = Inbox(app)
    data = inbox.getCustomer(id)
    inboxData = {}
    inboxData = inbox.getInboxDatas({'customer_id' : id})
    return render_template('inboxIndex.html', title = unicode("入库箱信息", 'utf-8'), data=data, inboxData=inboxData)
    #return json.dumps({'':inboxData})


@app.route('/addInbox', methods=['GET', 'POST'])
def addInbox():

    if request.method == 'POST':
        name = request.form['name']
        memo = request.form['memo']
        length = request.form['length']
        width = request.form['width']
        height = request.form['height']
        weight = request.form['weight']
        datas = {'name' : name,
                 'memo' : memo,
                 'length' : length,
                 'width' : width,
                 'height' : height,
                 'weight' : weight
                 }

        result = Inbox(app).addInbox(datas)
        if result:
            return redirect('/inboxIndex')
        else:
            return json.dumps({'error':result})
    else:
        return render_template('addInbox.html', title=unicode('入库箱追加', 'utf-8'))


@app.route('/customer')
def customer():

    customers = Customer(app).getCustomers()

    return render_template('customer.html', title = unicode("顾客信息", 'utf-8'),customersData = customers)

@app.route('/customerAdd', methods=['GET', 'POST'])
def customerAdd():

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
        id_confirmed_flag = request.form['id_confirmed_flag']
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

        result = Customer(app).insertCustomer(data)

        if result:
            return redirect("customer")


    return render_template('customerAdd.html', title = unicode("顾客信息", 'utf-8'))

@app.route('/customerEdit', methods=['GET', 'POST'])
def customerEdit():

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
        id_confirmed_flag = request.form['id_confirmed_flag']
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
            return redirect("customer")


    else:
        id = request.args.get('id')


    customer = Customer(app).getCustomer(int(id))

    return render_template('customerAdd.html', title = unicode("顾客信息", 'utf-8'),data = customer)


@app.route('/customerDelete', methods=['GET', 'POST'])
def customerDelete():
    if request.method == 'POST':
        id = request.form['id']

        data = {
            'delete_flag': 1
        }

        result = Customer(app).updateCustomer(data,int(id))
        if result:
            return redirect("customer")

    else:

        id = request.args.get('id')

    return render_template('customerDelete.html', title = unicode("确定删除", 'utf-8'), id = id)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
