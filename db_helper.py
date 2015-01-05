from pymongo import MongoClient

client = MongoClient()
db = client.account_manager

users = db.users

def user_auth(username, password):
    return users.find({'username':username, 'password':password}).count() == 1

def user_exists(username):
    return users.find({'username':username}).count() > 0

def user_creat(username, password):
    if (not user_exists(username)):
        new = { 'username' : username,
                'password' : password
                }
        users.insert(new)
        return "Registration successful"
    return "Registration failed; Username taken"

def get_pass(username):
    user = users.find_one({'username':username})
    if (user != None):
        return user['password']
