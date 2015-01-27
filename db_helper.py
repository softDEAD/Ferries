#from pymongo import MongoClient
from pymongo import Connection

#client = MongoClient()
#db = client.account_manager

conn = Connection()
db = conn['accountinfo']

users = db.users
orders = db.orders

#-----CHANGING ORDERID-----(you'd be kidding if you told me this was the best way to do this)
def up_id():
    f = open('orderid.txt')
    for line in f.readlines():
        i = int(line.strip())
    f.close()
    i = i+1
    f = open('orderid.txt', 'w')
    f.write(str(i))
    f.close()

def get_id():
    f = open('orderid.txt')
    for line in f.readlines():
        i = int(line.strip())
    f.close()
    return i

#-----USERNAMES-----
def user_auth(username, password): #string, string
    return users.find({'username':username, 'password':password}).count() == 1

def user_exists(username): #string
    return users.find({'username':username}).count() > 0

def user_creat(username, password): #string, string
    if (not user_exists(username)):
        new = { 'username' : username,
                'password' : password,
                'frees' : [],
                'lunch' : 0,
		'rep' : 0,
                'ordersplaced' : [],
		'ordersfulfilled' : [],
                'profilecomments' : [],
                'pendingorders' : []
                }
        users.insert(new)
        print "Registration successful"
    print "Registration failed; Username taken"

def change_frees(username, frees): #string, list
    users.update(
        {'username' : username},
        {"$set" : {'frees':frees}},
        upsert = True)

def change_lunch(username, lunch): #string, int
    users.update(
        {'username' : username},
        {"$set" : {'lunch':lunch}},
        upsert = True)
    
def get_user_data(username, data): #string, string
    user = users.find_one({'username':username})
    if (user != None):
        if data in user:
            return user[data]
    print "No %s data for user %s."%(data,username)

def get_all_user_data(username): #string
    user = users.find_one({'username':username})
    user.pop("password", None) #privacy is cool
    return user

def profile_comment(username, comment): #string, string
    users.update(
        {'username' : username},
        {"$push" : {'profilecomments':comment}},
    )

def plus_rep(username):
    users.update(
        {'username' : username},
        {"$set" : {'rep':user['rep']+1}},
        upsert = True)

def minus_rep(username):
    users.update(
        {'username' : username},
        {"$set" : {'rep':user['rep']-1}},
        upsert = True)

#-----ORDERS-----
def order_creat(orderid, username, store, food, cost,
                offer, preferredperiod,
                otherperiods, instructions): #int, string, string, string, float, float, int, list, string
    new = { 'orderid' : orderid,
            'username' : username,
            'store' : store,
            'food' : food, #predefined list?
            'cost' : cost, #calculated?
            'offer' : offer,
            'preferredperiod' : preferredperiod,
            'otherperiods' : otherperiods,
            'instructions' : instructions,
            'takenby' : '', #when taken by someone it displays as 'Taken by %s'
            'comments' : []
            }
    users.update(
        {'username' : username},
        {"$push" : {'ordersplaced':orderid}},
    )
    orders.insert(new)
    ################################spammable??
    print "Order #%s created"%(orderid)
    
def get_order_data(orderid, data): #int, string
    order = orders.find_one({'orderid':orderid})
    if (order != None):
        if data in order:
            return order[data]
    print "No %s data for order %d."%(data,orderid)

def get_all_order_data(orderid): #int
    return orders.find_one({'orderid':orderid})

def get_orders(store = '', period = 0): #string, int
    ret = [] #returns list of orderids
    if store == '':
        porders = orders.find({'period':period})
        for order in porders:
            ret.append(order['orderid'])
    elif period == 0:
        sorders = orders.find({'store':store})
        for order in sorders:
            ret.append(order['orderid'])
    else:
        psorders = orders.find({'store':store,
                                'period':period})
        for order in psorders:
            ret.append(order['orderid'])
    return ret

def order_fulfill(orderid): #int
    #username is the person who fulfilled order
    order = orders.find_one({'orderid':orderid})
    user = order['takenby']
    if not user_exists(user):
        print "Error, user not found"
        return -1
    users.update(
        {'username' : username},
        {"$push" : {'ordersfulfilled':orderid}},
    )
    orders.remove(order)

def take_order(username, orderid): #string, string
    order = orders.find_one({'orderid':orderid})
    if order['takenby'] != '':
        print "Order already taken by %s"%(order['takenby'])
        return -1
    users.update(
        {'username' : username},
        {"$push" : {'pendingorders':orderid}},
    )
    orders.update(
        {'orderid' : orderid},
        {"$set" : {'takenby':username}},
        upsert = True)
    print "Order taken"


def add_comment(comment, orderid, username):
    orders.update(
        {'orderid' : orderid},
        {"$push" : {'comments':[username, comment]}},
    )
    print "Comment added"



