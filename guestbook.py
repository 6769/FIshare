import shelve
import sys

DATA_FILE = 'guestbook'
TAG_LIST=   'greeting_list'

def save_data( comment, create_at):
    """
    save data from form submitted
    """
    with shelve.open(DATA_FILE) as database: 
        if TAG_LIST not in database:
            greeting_list = []
        else:
            greeting_list = database[TAG_LIST]
        greeting_list.insert(
            0, { 'comment': comment, 'create_at': create_at})
        database[TAG_LIST] = greeting_list
    

def load_data():
    """
    load saved data
    """
    with shelve.open(DATA_FILE) as database:
        greeting_list = database.get(TAG_LIST, [])
    return greeting_list
def delete_data(msgindex):
    with shelve.open(DATA_FILE) as database:
        greeting_list = database.get(TAG_LIST, [])
        print(type(greeting_list))
        print(greeting_list)
        msgindex=int(msgindex)
        del greeting_list[msgindex]
        database[TAG_LIST] = greeting_list
    