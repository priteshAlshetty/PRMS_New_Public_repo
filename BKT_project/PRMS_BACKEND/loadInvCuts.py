import mysql.connector as conn
from openpyxl import load_workbook
from openpyxl.formula import Tokenizer
from datetime import datetime

# add cuts manually to required cuts of ply
connection = conn.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
    )
def loadInvCutsToProd():
    if connection.is_connected:
        cursor = connection.cursor()
        cursor.execute('SELECT `PROD_ID` FROM `recipe_inv` WHERE 1')
        result= cursor.fetchall()
        PROD_ID = result
        try:
            for id_tuple in PROD_ID:
                id = id_tuple[0]
                cursor.execute("SELECT * FROM `recipe_inv` WHERE `PROD_ID` =%s ", [id])
                invcuts = cursor.fetchone()
                invcuts = tuple(invcuts[1:])
                # invcuts = tuple(invcuts[:-1])
                params = list(invcuts) + [id]
                
                cursor.execute('''UPDATE `recipe_prod` SET
                            `REQ_CUTS_PLY_1` = `REQ_CUTS_PLY_1`+%s,
                            `REQ_CUTS_PLY_2` = `REQ_CUTS_PLY_2`+%s,
                            `REQ_CUTS_PLY_3` = `REQ_CUTS_PLY_3`+%s,
                            `REQ_CUTS_PLY_4` = `REQ_CUTS_PLY_4`+%s,
                            `REQ_CUTS_PLY_5` = `REQ_CUTS_PLY_5`+%s,
                            `REQ_CUTS_PLY_6` = `REQ_CUTS_PLY_6`+%s,
                            `REQ_CUTS_PLY_7` = `REQ_CUTS_PLY_7`+%s,
                            `REQ_CUTS_PLY_8` = `REQ_CUTS_PLY_8`+%s,
                            `REQ_CUTS_PLY_9` = `REQ_CUTS_PLY_9`+%s,
                            `REQ_CUTS_PLY_10` = `REQ_CUTS_PLY_10`+%s,
                            `REQ_CUTS_PLY_11` = `REQ_CUTS_PLY_11`+%s,
                            `REQ_CUTS_PLY_12` = `REQ_CUTS_PLY_12`+%s,
                            `REQ_CUTS_PLY_13` = `REQ_CUTS_PLY_13`+%s,
                            `REQ_CUTS_PLY_14` = `REQ_CUTS_PLY_14`+%s
                            
                        WHERE `PROD_ID` = %s ''',invcuts+(id,))
                print(f"Inv Cuts added for prod id:{id}")
                
            return True
                
        except Exception as e:
            print(f"ERROR at loadInvCutsToProd():{e} ")
            return False
            
# loadInvCutsToProd()