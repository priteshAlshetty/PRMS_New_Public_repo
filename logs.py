
from openpyxl import load_workbook
from datetime import datetime

# updateRecipe("D:\\BKT_PRMS\\RECIPE_1.xlsx")
def saveLogs(log:str):
    try:
        # Load the workbook
        wb = load_workbook("C:\\BKT_Bias_cutter_3\\Book1.xlsx")
        
        # Select the worksheet
        ws = wb["Sheet1"]
        # Create a timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Save the workbook
        
        ws.append([timestamp,log])
        wb.save("C:\\BKT_Bias_cutter_3\\Book1.xlsx")
        return 1  # Return 1 to indicate success
    except Exception as e:
        print(f"An error occurred while saving logs: {e}")
        return 0  # Return 0 to indicate failure
saveLogs("save")