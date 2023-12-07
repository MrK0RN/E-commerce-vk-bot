import pymysql

#6Gjw8gD3hks

from config import MYSQL_HOST as host, MYSQL_PASSWORD as password, MYSQL_USER as user, MYSQL_DBNAME as dbname, MYSQL_PORT as port
def connect(a):
    try:
        mysql = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Conn Succ")
        if (a == 0):
            mysql.close()
    except Exception as error:
        print("Conn Err \n"+str(error))

class mysqli:
    try:
        mysqlconnection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Conn Succ")
    except Exception as error:
        print("Conn Err \n"+str(error))
    def query(self, query, k):
        with self.mysqlconnection.cursor() as cursor:
            cursor.execute(query, k)
            self.mysqlconnection.commit()
            try:
                rows = cursor.fetchall()
                i = 0
                ans = []
                for row in rows:
                    ans.append(row)
                return ans
            except Exception:
                pass

    def close(self):
        self.mysqlconnection.close()