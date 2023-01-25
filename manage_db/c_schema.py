import mysql.connector
from mysql.connector.errors import Error

try: 
    connection = mysql.connector.connect(host = 'localhost',
                                user= 'root',
                                password = '02749')




    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE test_fit ")
except (Exception , mysql.connector.Error) as error :
    print("Error while creating Schema :  " ,error)


finally : 
    cursor.close()
    connection.close()
    print("MYSQL connection is closed")
