import mysql.connector
from pprint import pprint
conn = mysql.connector.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
)

print('connected to wampserver')
cursor = conn.cursor()
cursor.execute("SELECT  * FROM `recipe_prod` WHERE `PROD_ID` = %s", ["1109"])
result = cursor.fetchone()

pprint(result[3:])