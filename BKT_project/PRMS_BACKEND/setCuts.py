from openpyxl import load_workbook 
import mysql.connector 
# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
)
def setCutsUpdate(connection, selectData:list):
    # Check if the connection was successful
    # script to update and insert schedule on server
    if connection.is_connected():
        print("Connected to MySQL database")
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        selectData = selectData[1:]  #drop column names
        PROD_ID = list()
        try:
            for item in selectData:
                PROD_ID.append(
                (str(item[1]),
                item[-1])
                )
        except Exception as e:
            print(f"error at calculating PROD_ID:{e}")
        setCuts = list()
        row =list()
    else:
        print("error in connecting wampserver")
    
    for id in PROD_ID:
        sql = "SELECT  `CONV_1`, `CONV_2`, `CONV_3`, `CONV_4`, `CONV_5`, `CONV_6`, `CONV_7`, `CONV_8`, `CONV_9`, `CONV_10`, `CONV_11`, `CONV_12`, `CONV_13`, `CONV_14` FROM `recipe_conv_table` WHERE `PROD_ID` = %s"
        cursor.execute(sql, [id[0]])
        convList = cursor.fetchone()       
        if convList :
            row = [id[1] for _ in range(14)]
            for conv in convList:
                cuts = 1 + (id[1] * conv)
                setCuts.append(cuts)
            row = row + setCuts # appending two list
            row.insert(0, id[0])
            cursor.execute("SELECT * FROM `recipe_prod` WHERE `PROD_ID` =%s", [id[0]])
            flag = cursor.fetchone()
            if flag!= None:
                try:
                    cursor.execute("""UPDATE `recipe_prod` SET 
                                    `SET_TYRES_PLY_1`= %s, `SET_TYRES_PLY_2`=%s, `SET_TYRES_PLY_3`=%s, `SET_TYRES_PLY_4`=%s, `SET_TYRES_PLY_5`=%s, `SET_TYRES_PLY_6`=%s, `SET_TYRES_PLY_7`=%s, `SET_TYRES_PLY_8`=%s, `SET_TYRES_PLY_9`=%s, `SET_TYRES_PLY_10`=%s, `SET_TYRES_PLY_11`=%s , `SET_TYRES_PLY_12`=%s , `SET_TYRES_PLY_13`=%s , `SET_TYRES_PLY_14`=%s , `SET_CUTS_PLY_1`=`REQ_CUTS_PLY_1`+ %s , `SET_CUTS_PLY_2`=`REQ_CUTS_PLY_2`+ %s , `SET_CUTS_PLY_3`=`REQ_CUTS_PLY_3`+ %s , `SET_CUTS_PLY_4`=`REQ_CUTS_PLY_4`+ %s , `SET_CUTS_PLY_5`=`REQ_CUTS_PLY_5`+ %s , `SET_CUTS_PLY_6`=`REQ_CUTS_PLY_6`+ %s , `SET_CUTS_PLY_7`=`REQ_CUTS_PLY_7`+ %s , `SET_CUTS_PLY_8`=`REQ_CUTS_PLY_8`+ %s , `SET_CUTS_PLY_9`=`REQ_CUTS_PLY_9`+ %s , `SET_CUTS_PLY_10`=`REQ_CUTS_PLY_10`+ %s , `SET_CUTS_PLY_11`=`REQ_CUTS_PLY_11`+ %s , `SET_CUTS_PLY_12`=`REQ_CUTS_PLY_12`+ %s , `SET_CUTS_PLY_13`=`REQ_CUTS_PLY_13`+ %s , `SET_CUTS_PLY_14`=`REQ_CUTS_PLY_14`+ %s WHERE `PROD_ID` =%s""", row[1:] + [id[0]] )
                except Exception as e:
                    print(e)
            else:
                try:
                    sql = "INSERT INTO recipe_prod ( `PROD_ID`, `SET_TYRES_PLY_1`, `SET_TYRES_PLY_2`, `SET_TYRES_PLY_3`, `SET_TYRES_PLY_4`, `SET_TYRES_PLY_5`, `SET_TYRES_PLY_6`, `SET_TYRES_PLY_7`, `SET_TYRES_PLY_8`, `SET_TYRES_PLY_9`, `SET_TYRES_PLY_10`, `SET_TYRES_PLY_11`, `SET_TYRES_PLY_12`, `SET_TYRES_PLY_13`, `SET_TYRES_PLY_14`, `SET_CUTS_PLY_1`, `SET_CUTS_PLY_2`, `SET_CUTS_PLY_3`, `SET_CUTS_PLY_4`, `SET_CUTS_PLY_5`, `SET_CUTS_PLY_6`, `SET_CUTS_PLY_7`, `SET_CUTS_PLY_8`, `SET_CUTS_PLY_9`, `SET_CUTS_PLY_10`, `SET_CUTS_PLY_11`, `SET_CUTS_PLY_12`, `SET_CUTS_PLY_13`, `SET_CUTS_PLY_14`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, row)
                except Exception as e: 
                    print(e)
            setCuts = []
        else:
            print(f"Conv_factors not found for PROD_ID {id[0]}")
            id_remove = id[0]
            PROD_ID.remove(id_remove)
            
        
        # updating Req_cuts from Set_cuts
    for id in PROD_ID:
        try:
            cursor.execute (""" UPDATE `recipe_prod` SET 
                                `REQ_CUTS_PLY_1` = `SET_CUTS_PLY_1` ,`REQ_CUTS_PLY_2` = `SET_CUTS_PLY_2`,`REQ_CUTS_PLY_3` = `SET_CUTS_PLY_3` ,`REQ_CUTS_PLY_4` = `SET_CUTS_PLY_4`,`REQ_CUTS_PLY_5` = `SET_CUTS_PLY_5` ,`REQ_CUTS_PLY_6` = `SET_CUTS_PLY_6`,`REQ_CUTS_PLY_7` = `SET_CUTS_PLY_7` ,`REQ_CUTS_PLY_8` = `SET_CUTS_PLY_8`,`REQ_CUTS_PLY_9` = `SET_CUTS_PLY_9` ,`REQ_CUTS_PLY_10` = `SET_CUTS_PLY_10`,`REQ_CUTS_PLY_11` = `SET_CUTS_PLY_11` ,`REQ_CUTS_PLY_12` = `SET_CUTS_PLY_12`,`REQ_CUTS_PLY_13` = `SET_CUTS_PLY_13` ,`REQ_CUTS_PLY_14` = `SET_CUTS_PLY_14` WHERE `PROD_ID` = %s""" ,(id[0],))
        except Exception as e:
            print(f"error at setCuts(),updating Req_cuts:{e}" )
    print('done!')
    cursor.close()
    connection.close()

