import mysql.connector as conn
connection = conn.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
)

def delete_Data():
    connection = conn.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute( "DELETE FROM `recipe_1_select` WHERE 1")
        cursor.execute( "DELETE FROM `recipe_conv_table` WHERE 1")
        cursor.execute( "DELETE FROM `recipe_width` WHERE 1")
        cursor.execute( "DELETE FROM `recipe_prod` WHERE 1")
        
        return 1
    else:
        return "connection to wamp server failed"