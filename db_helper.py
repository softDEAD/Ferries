from pymongo import MongoClient

client = MongoClient()
db = client.account_manager

users = db.users
orders = db.orders

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
        return "Registration successful"
    return "Registration failed; Username taken"

def change_frees(username, frees): #string, list
    user = users.find_one({'username':username})
    users.update(
        {'username' : username},
        {"$set" : {'frees':frees}},
        upsert = True)

def change_lunch(username, lunch): #string, int
    user = users.find_one({'username':username})
    users.update(
        {'username' : username},
        {"$set" : {'lunch':lunch}},
        upsert = True)
    
def get_user_data(username, data): #string, string
    user = users.find_one({'username':username})
    if (user != None):
        if data in user:
            return user[data]
    return "No %s data for user %s."%(data,username)

def get_all_user_data(username): #string
    user = users.find_one({'username':username})
    ret = []
    if (user != None):
        for var in user:
            if (var != "password"): #privacy is cool
                ret.append(var)
    return ret

def profile_comment(username, comment): #string, string
    users.update(
        {'username' : username},
        {"$push" : {'profilecomments':comment}},
    )

    
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
            'takenby' : None, #when taken by someone (if not None) it displays as 'Taken by %s'
            'comments' : []
            }
    users.update(
        {'username' : username},
        {"$push" : {'ordersplaced':orderid}},
    )
    orders.insert(new)
    ################################spammable??
    return "Order #%s created"%(orderid)

def get_order_data(orderid, data): #int, string
    order = orders.find_one({'orderid':orderid})
    if (order != None):
        if data in order:
            return order[data]
    return "No %s data for order %d."%(data,orderid)

def get_all_order_data(orderid): #int
    order = orders.find_one({'orderid':orderid})
    ret = []
    if (order != None):
        for var in order:
            ret.append(order[var])
    return ret

def get_orders(stores, periods): #list, list
    ret = [] #returns list of orderids
    if len(stores) == 0:
        for period in periods:
            orders = orders.find({'period':period})
        for order in orders:
            ret.append(order['orderid'])
    elif len(periods) == 0:
        for store in stores:
            orders = orders.find({'store':stores})
            for order in orders:
                ret.append(order['orderid'])
    else:
        for store in stores:
            for period in periods:
                orders = orders.find({'store':store,
                                      'period':period})
                for order in orders:
                    ret.append(order['orderid'])
    return ret

def order_fulfill(orderid): #int
    #username is the person who fulfilled order
    order = orders.find_one({'orderid':orderid})
    user = order['takenby']
    if not user_exists(user):
        return "Error, user not found"
    users.update(
        {'username' : username},
        {"$push" : {'ordersfulfilled':orderid}},
    )
    orders.remove(order)

def take_order(username, orderid): #string, string
    user = users.find_one({'username':username})
    order = orders.find_one({'orderid':orderid})
    if order['takenby'] != None:
        return "Order already taken by %s"%(order['takenby'])
    users.update(
        {'username' : username},
        {"$push" : {'pendingorders':orderid}},
    )
    orders.update(
        {'orderid' : orderid},
        {"$set" : {'takenby':username}},
        upsert = True)
    return "Order taken"

def add_comment(comment, orderid):
    orders.update(
        {'orderid' : orderid},
        {"$push" : {'comments':comment}},
    )
    return "Comment added"



