import mysql


def get_current_goods():
    db = mysql.mysqli()
    z = db.query("SELECT * FROM `GOODS` WHERE `remain` > 0;", k = [])
    print(z)
    return z

get_current_goods()