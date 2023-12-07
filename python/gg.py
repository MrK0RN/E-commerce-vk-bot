import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=8889,
        user='root',
        passwd='root',
        database='yzzme_35577374_vk_bot',
    )
    print("successfully connected...")
    print("#" * 20)

except Exception as ex:
    print("Connection refused...")
    print(ex)
