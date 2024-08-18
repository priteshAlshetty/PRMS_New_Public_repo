from datetime import datetime
import mysql.connector
from pprint import pprint
def getDetails(id:str):
    dict_obj = dict()
    dict_obj['timestamp'] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_obj['prod_id'] = id
    conn = mysql.connector.connect(
    host="localhost",
    user="backend_comm",
    database="bkt_prms",
    port ="3306",
    password ="ASD-90K-10B8"
)
    try:
        if conn.is_connected():
            print('connected to wampserver')
            cursor = conn.cursor()
            cursor.execute("SELECT  * FROM `recipe_1_select` WHERE `PROD_ID` = %s", [str(id)])
            result = cursor.fetchone()
            cursor.execute('SELECT * FROM `recipe_prod` WHERE `PROD_ID`=%s ', [str(id)])
            tyres = cursor.fetchone()
            if(result):
                dict_obj['prod_id'] =  str(result[1])
                dict_obj['size'] =  str(result[2])
                dict_obj['Fabric_1'] =  str(result[3])
                dict_obj['Fabric_2'] =  str(result[4])
                dict_obj['Fabric_3'] =  str(result[5])
                dict_obj['Fabric_4'] =  str(result[6])
                dict_obj['Fabric_5'] =  str(result[7])
                dict_obj['Fabric_6'] =  str(result[8])
                dict_obj['Fabric_7'] =  str(result[9])
                dict_obj['Fabric_8'] =  str(result[10])
                dict_obj['Fabric_9'] =  str(result[11])
                dict_obj['Fabric_10'] =  str(result[12])
                dict_obj['Fabric_11'] =  str(result[13])
                dict_obj['Fabric_12'] =  str(result[14])
                dict_obj['Fabric_13'] =  str(result[15])
                dict_obj['Fabric_14'] =  str(result[16])
                dict_obj['tyres'] =  str(result[17])
                dict_obj['setTyres_PLY_1'] =  str(tyres[3])
                dict_obj['setTyres_PLY_2'] =  str(tyres[4])
                dict_obj['setTyres_PLY_3'] =  str(tyres[5])
                dict_obj['setTyres_PLY_4'] =  str(tyres[6])
                dict_obj['setTyres_PLY_5'] =  str(tyres[7])
                dict_obj['setTyres_PLY_6'] =  str(tyres[8])
                dict_obj['setTyres_PLY_7'] =  str(tyres[9])
                dict_obj['setTyres_PLY_8'] =  str(tyres[10])
                dict_obj['setTyres_PLY_9'] =  str(tyres[11])
                dict_obj['setTyres_PLY_10'] =  str(tyres[12])
                dict_obj['setTyres_PLY_11'] =  str(tyres[13])
                dict_obj['setTyres_PLY_12'] =  str(tyres[14])
                dict_obj['setTyres_PLY_13'] =  str(tyres[15])
                dict_obj['setTyres_PLY_14'] =  str(tyres[16])
                dict_obj['setCuts_1'] =  str(tyres[17]) if tyres[17] is not None else 0
                dict_obj['setCuts_2'] =  str(tyres[18])  if tyres[18] is not None else 0
                dict_obj['setCuts_3'] =  str(tyres[19])  if tyres[19] is not None else 0
                dict_obj['setCuts_4'] =  str(tyres[20])  if tyres[20] is not None else 0
                dict_obj['setCuts_5'] =  str(tyres[21])  if tyres[21] is not None else 0
                dict_obj['setCuts_6'] =  str(tyres[22])  if tyres[22] is not None else 0
                dict_obj['setCuts_7'] =  str(tyres[23])  if tyres[23] is not None else 0
                dict_obj['setCuts_8'] =  str(tyres[24])  if tyres[24] is not None else 0
                dict_obj['setCuts_9'] =  str(tyres[25])  if tyres[25] is not None else 0
                dict_obj['setCuts_10'] =  str(tyres[26])  if tyres[26] is not None else 0
                dict_obj['setCuts_11'] =  str(tyres[27])  if tyres[27] is not None else 0
                dict_obj['setCuts_12'] =  str(tyres[28])  if tyres[28] is not None else 0
                dict_obj['setCuts_13'] =  str(tyres[29])  if tyres[29] is not None else 0
                dict_obj['setCuts_14'] =  str(tyres[30])  if tyres[30] is not None else 0
                
                dict_obj['message']=f"Info retived for ID: {result[1]}"
            else:
                dict_obj['error']= f"Error retriving Data for ID:{id} , either PROD_ID is wrong or ID not found on server!!"
                
            
    except Exception as e:
        dict_obj['error']=f'Exception raised in backend Function getDetails()'
        dict_obj['exception']=f'{e}'
    
    return dict_obj    
        
