import config
import random
import string

import mysql


def Make_key():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(config.KEY_LENGTH))

def get_link(emails):
    key = Make_key()

    db = mysql.mysqli()

    db.query("UPDATE key WHERE email = %s;", [emails])
