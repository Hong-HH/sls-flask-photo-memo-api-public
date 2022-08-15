import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(host ='',
                                        database = '',
                                        user = '',
                                        password = '')
    return connection