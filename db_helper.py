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

def user_creat(username, password, frees, lunch, rep, ordersplaced, ordersfulfilled, profilecomments): #string, string, list, int, int, int, int, list
    if (not user_exists(username)):
        new = { 'username' : username,
                'password' : password,
                'frees' : free,
                'lunch' : lunch,
		'rep' : 0,
                'ordersplaced' : 0,
		'ordersfulfilled' : 0,
                'profilecomments' : []
                }
        users.insert(new)
        return "Registration successful"
    return "Registration failed; Username taken"

def get_data(username, data): #string, string
    user = users.find_one({'username':username})
    if (user != None):
        if data in user:
            return user[data]
        return "No %s data for user %s."%(data,username)

def profile_comment(username, comment): #string, string
    user = users.findone({'username':username})
    comments = user['profilecomments']
    comments.append(comment)
    
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
            'instructions' : instructions
            } #how do we note that an order has been taken up by someone?
    orders.insert(new)
    return "Order #%s created"%(orderid)

def get_orders(stores, periods): #list, list
    ret = []
    if len(stores) == 0:
        for period in periods:
            ret.append(orders.find({'period':period}))
    elif len(periods) == 0:
        for store in stores:
            ret.append(orders.find({'store':stores}))
    else:
        for store in stores:
            for period in periods:
                ret.append(orders.find({'store':store,
                                        'period':period}))
    return ret

def order_fulfill(orderid): #int
    #username is the person who fulfilled order
    order = orders.findone({'orderid':orderid})
    db.orders.remove(order)
    




