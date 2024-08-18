import pandas as pd
import mysql.connector as conn
from mysql.connector import Error
from datetime import datetime
import os

SAVE_DIR ="C:\\Reports"

def export_to_excel():
    """
    Connects to a MySQL database, fetches data from specified tables,
    and exports the data to an Excel file.

    Parameters:
    - host (str): The host of the MySQL database.
    - user (str): The user of the MySQL database.
    - database (str): The name of the MySQL database.
    - port (str): The port of the MySQL database.
    - save_directory (str): The directory where the Excel file will be saved.

    Returns:
    - str: The path of the created Excel file or an error message.
    """
    try:
        # MySQL connection parameters
        connection = conn.connect(
        host="localhost",
        user="backend_comm",
        database="bkt_prms",
        port ="3306",
        password ="ASD-90K-10B8"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Dictionary to store DataFrames for each table
            dataframes = {}
            # Tables and corresponding sheet names
            tables = {
                "recipe_1_select": "recipe_1_select",
                "recipe_conv_table": "recipe_conv",
                "recipe_width": "recipe_width"
            }
            for table_name, sheet_name in tables.items():
                # Query to fetch data from each table
                query = f"SELECT * FROM `{table_name}`"
                cursor.execute(query)
                # Fetch all records
                records = cursor.fetchall()
                # Get column names for DataFrame creation
                column_names = [i[0] for i in cursor.description]
                # Create a DataFrame from the fetched records
                df = pd.DataFrame(records, columns=column_names)
                # Store the DataFrame in the dictionary with sheet name as key
                dataframes[sheet_name] = df
            # Generate timestamp for filename
            
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # new_file = f"recipe_{timestamp}.xlsx"
            new_file = f"recipe_sample.xlsx"
            
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)
            # Specify path and filename for the Excel file
            excel_file = os.path.join(SAVE_DIR, new_file)
            # Check if a previous file exists and remove it
            if os.path.exists(excel_file):
                os.remove(excel_file)
            # Create a Pandas Excel writer using XlsxWriter as the engine
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                # Write each DataFrame to a specific sheet
                for sheet_name, df in dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            # return new_file
            
    except Error as e:
        return -1
    except Exception as ex:
        return -1
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection is not None and connection.is_connected():
            connection.close()
    
    return new_file
    # return 0


# Call the function to export data to Excel
# exported_file = export_to_excel()
# print(f'Exported file: {exported_file}')

