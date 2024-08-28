import mysql.connector as conn
from mysql.connector import Error
from datetime import datetime
import openpyxl
import os

def get_conv_value(cursor, prod_id, ply_braker):
    conv_column = f'CONV_{ply_braker}'
    conv_query = f"SELECT {conv_column} FROM recipe_conv_table WHERE PROD_ID = %s"
    
    cursor.execute(conv_query, (prod_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"No CONV value found for PROD_ID={prod_id} and PLY_BRAKER={ply_braker}")
        return None

def get_size(cursor, prod_id):
    size_query = "SELECT SIZE FROM recipe_1_select WHERE PROD_ID = %s"
    
    cursor.execute(size_query, (prod_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"No SIZE found for PROD_ID={prod_id}")
        return None

def get_fabric_name(cursor, prod_id, ply_braker):
    fabric_name = "None"
    if 1 <= ply_braker <= 10:
        column_name = f'FABRIC_PLY_{ply_braker}'
    elif 11 <= ply_braker <= 14:
        column_name = f'FABRIC_BRAKER_{ply_braker}'
    else:
        return fabric_name

    query = f"SELECT {column_name} FROM recipe_1_select WHERE PROD_ID = %s"
    cursor.execute(query, (prod_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        fabric_name = result[0]
    
    return fabric_name

def get_width(cursor, prod_id, ply_braker):
    width_column = f'WIDTH_{ply_braker}'
    try:
        query = f"SELECT {width_column} FROM recipe_width WHERE PROD_ID = %s"
        cursor.execute(query, (prod_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"No width found for PROD_ID={prod_id} and PLY_BRAKER={ply_braker}")
            return None
    except Error as e:
        print(f"Error retrieving width: {e}")
        return None

def get_angle(cursor, prod_id, ply_braker):
    angle_query = f"SELECT ANGLE_{ply_braker} FROM recipe_conv_table WHERE PROD_ID = %s"
    
    cursor.execute(angle_query, (prod_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"No ANGLE value found for PROD_ID={prod_id} and PLY_BRAKER={ply_braker}")
        return None

def insert_new_record(connection, entry, size, fabric_name, width, angle):
    date_curr = entry['date_curr'].strftime('%Y-%m-%d')
    prod_id = entry['PROD_ID']
    ply_braker = entry['PLY_BRAKER']
    shift = entry['Shift']
    manual_cuts = entry['Manual_Cuts']
    length = entry['Length']
    
    conv_value = get_conv_value(connection.cursor(), prod_id, ply_braker)
    if conv_value is not None and conv_value != 0:
        tyer = manual_cuts / conv_value
        remain_tyres = tyer
    else:
        tyer = 0
        remain_tyres = 0

    try:
        cursor = connection.cursor()
        set_cuts_column = f'SET_CUTS_PLY_{ply_braker}'  
        set_tyres_column = f'SET_TYRES_PLY_{ply_braker}'

        set_cuts_query = f"SELECT {set_cuts_column} FROM recipe_prod WHERE PROD_ID = %s"
        cursor.execute(set_cuts_query, (prod_id,))
        set_cuts_result = cursor.fetchone()
        total_set_cuts = set_cuts_result[0] if set_cuts_result else 0

        set_tyres_query = f"SELECT {set_tyres_column} FROM recipe_prod WHERE PROD_ID = %s"
        cursor.execute(set_tyres_query, (prod_id,))
        set_tyres_result = cursor.fetchone()
        total_set_tyres = set_tyres_result[0] if set_tyres_result else 0
        
        remain_cuts_col = f'REQ_CUTS_PLY_{ply_braker}'  
        remain_cuts_query = f"SELECT {remain_cuts_col} FROM recipe_prod WHERE PROD_ID = %s"
        cursor.execute(remain_cuts_query, (prod_id,))
        remain_cuts_result =cursor.fetchone()
        remain_cuts = remain_cuts_result[0] if remain_cuts_result else 0
        remain_cuts = remain_cuts - manual_cuts
        
    except Error as e:
        print(f"Error retrieving total_set_cuts or total_set_tyres: {e}")
        total_set_cuts = 0
        total_set_tyres = 0
    finally:
        cursor.close()

    insert_query = """
        INSERT INTO recipe_report  (date_curr, PROD_ID, PLY_BRAKER, Shift, act_cuts, remain_cuts, act_tyres, remain_tyres, SIZE, FABRIC_NAME, WIDTH, ANGLE, total_set_cuts, total_set_tyres,Length)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """
    
    cursor = connection.cursor()
    cursor.execute(insert_query, (date_curr, prod_id, ply_braker, shift, manual_cuts, remain_cuts, tyer, remain_tyres, size, fabric_name, width, angle, total_set_cuts, total_set_tyres, length))
    connection.commit()
    cursor.close()
    print(f"Inserted new record: date_curr={date_curr}, PROD_ID={prod_id}, PLY_BRAKER={ply_braker}, Shift={shift}, Manual_Cuts={manual_cuts}, TYER={tyer}, Total_Set_Cuts={total_set_cuts}, Total_Set_Tyres={total_set_tyres}")

def update_recipe_report(connection, entry):
    date_curr = entry['date_curr'].strftime('%Y-%m-%d')
    prod_id = entry['PROD_ID']
    ply_braker = entry['PLY_BRAKER']
    shift = entry['Shift']
    manual_cuts = entry['Manual_Cuts']
    length = entry['Length']
    

    print(f"Checking: date_curr={date_curr}, PROD_ID={prod_id}, PLY_BRAKER={ply_braker}, Shift={shift}")

    try:
        cursor = connection.cursor()

        check_query = """
            SELECT COUNT(*)
            FROM recipe_report 
            WHERE date_curr = %s AND PROD_ID = %s AND PLY_BRAKER = %s AND Shift = %s
        """  
        
        cursor.execute(check_query, (date_curr, prod_id, ply_braker, shift))
        count = cursor.fetchone()[0]
        print(f"Matching records count: {count}")
            
        if count > 0:
            conv_value = get_conv_value(cursor, prod_id, ply_braker)
            if conv_value is not None and conv_value != 0:
                tyer = manual_cuts / conv_value  # calculate tyres equivalent to cuts
                print(f"Calculated TYER: {tyer}")

                current_tyre_query = """
                    SELECT act_tyres, remain_tyres
                    FROM recipe_report 
                    WHERE date_curr = %s AND PROD_ID = %s AND PLY_BRAKER = %s AND Shift = %s
                """
                cursor.execute(current_tyre_query, (date_curr, prod_id, ply_braker, shift))
                current_values = cursor.fetchone()

                

                if current_values:
                    current_act_tyer, current_remain_tyer = current_values
                    new_act_tyer = current_act_tyer + tyer         # logic for syncing tyres based on cuts
                    new_remain_tyer = current_remain_tyer - tyer

                    update_query = """
                        UPDATE recipe_report 
                        SET act_cuts = act_cuts + %s, remain_cuts = remain_cuts - %s, 
                            act_tyres = %s, remain_tyres = %s, Length =%s
                        WHERE date_curr = %s AND PROD_ID = %s AND PLY_BRAKER = %s AND Shift = %s 
                    """
                    
                    cursor.execute(update_query, (manual_cuts, manual_cuts, new_act_tyer, new_remain_tyer,length, date_curr, prod_id, ply_braker, shift))
                    connection.commit()
                    print(f"Updated: date_curr={date_curr}, PROD_ID={prod_id}, PLY_BRAKER={ply_braker}, Shift={shift}, Manual_Cuts={manual_cuts}, TYER={tyer}")
                else:
                    print(f"No TYER values found for date_curr={date_curr}, PROD_ID={prod_id}, PLY_BRAKER={ply_braker}, Shift={shift}")
            else:
                print(f"Skipping update for PROD_ID={prod_id} due to missing or invalid CONV value.")
        else:
            #insert new record of cuts if not found
            size = get_size(cursor, prod_id)
            fabric_name = get_fabric_name(cursor, prod_id, ply_braker)
            width = get_width(cursor, prod_id, ply_braker)
            angle = get_angle(cursor, prod_id, ply_braker)
            
            if size and fabric_name and width and angle:
                insert_new_record(connection, entry, size, fabric_name, width, angle)
            else:
                print(f" At manual cuts backend code, new entry insertion:Cannot insert new record for PROD_ID={prod_id}, because '{prod_id}' not present in recipeschdule")
        
        # update cuts on recipe_prod also
        req_cuts_col = f'REQ_CUTS_PLY_{ply_braker}'  
        query = f"UPDATE `recipe_prod` SET `{req_cuts_col}` = `{req_cuts_col}`- {manual_cuts} WHERE  `PROD_ID` = {prod_id}"
        print(f"here:{query}")
        cursor.execute(query)
        
    except Error as e:
        print(f"Database error during update at Manual cuts Backend code: {e}")
        
    finally:
        if cursor:
            cursor.close()

def syncManualCuts(file_path):
    """
    Upload and process manual cuts from the given Excel file path.
    """
    connection = None
    try:
        connection = conn.connect(
            host="localhost",
            user="root",
            database="bkt_prms",
            port="3306"
        )

        if connection.is_connected():
            print("Connected to MySQL database")

            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active

            headers = [cell.value for cell in sheet[1]]
            print("Headers found in Excel file:", headers)

            if any(header is None for header in headers):
                print("Error: Some header names are missing or None.")
                return False

            header_map = {
                'date_curr': 'date_curr',
                'PROD_ID': 'PROD_ID',
                'PLY/BRAKER NO': 'PLY_BRAKER',
                'Shift': 'Shift',
                'Manual Cuts': 'Manual_Cuts',
                'Length': 'Length'
            }
        
            data = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                row_dict = {header_map.get(headers[i], headers[i]): row[i] for i in range(len(headers))}
                data.append(row_dict)

            print("Data extracted from Excel:", data)

            for entry in data:
                print(f"entries:\n{entry}")
                update_recipe_report(connection, entry)
                

            return True

    except Error as e:
        print(f"Connection or execution error: {e}")
        return False
    # finally:
    #     if connection and connection.is_connected():
    #         connection.close()
    #         print("MySQL connection closed")


# syncManualCuts('BKT_project\\PRMS_BACKEND\\manual.xlsx')