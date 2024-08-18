from flask import Flask, render_template ,request, jsonify,session,send_file,make_response
import os, sys
import datetime
from pprint import pprint
# user defined
from PRMS_BACKEND.schduleUpdate import updateRecipe,saveLogs
from PRMS_BACKEND.deleteData import delete_Data
from PRMS_BACKEND.getDetailsById import getDetails
from PRMS_BACKEND.loadInvCuts import loadInvCutsToProd
from PRMS_BACKEND.recipeDownload import export_to_excel
from PRMS_BACKEND.invCuts import uploadInvCuts
from PRMS_BACKEND.downloadReport import downloadCutReport

filepath = list()

app = Flask(__name__)
app.secret_key = "ASH-950-OL"

@app.route('/')# recipe upload screen
def serve_home():
    return render_template('index1.html')

@app.route('/home')# recipe upload screen
def serve_index():
    return render_template('index1.html')

@app.route('/serve-inv-cuts')# inv cuts screen
def serve_inv_cuts():
    return render_template('inv_cuts.html')


@app.route('/serve-view-edit')# view and edit screen
def serve_view_edit():
    return render_template('view_edit.html')

@app.route('/send_prod_id', methods=['POST'])
def receive_prod_id():
    data = request.get_json()
    prod_id = data.get('prodId')
    print(f"Received Product ID: {prod_id}")
    return jsonify({"message": "Product ID received"}), 200

@app.route('/upload_recipe', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename =='':
        return jsonify({'message':'no selected file'}),400
        
    # Ensure the file is an xlsx file
    if file.filename.endswith('.xlsx'):
        # Define the target directory
        target_dir = 'schedule'
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        # Generate a unique filename
        filename = f"{file.filename}"
        file_path = os.path.join(target_dir, filename)
        
        # Save the file
        file.save(file_path)
        # to store file path
        session['recipe_xlsx'] = file_path
        saveLogs(log="Recipe selected to upload on server")
        # Return the file path
        return jsonify({'message': file_path, 'timestamp':str(datetime.datetime.now())[:-6]}), 200
    else:
        return jsonify({  'timestamp':str(datetime.datetime.now())[:-6] , 'message': 'Wrong FILE', 'error':' only .xlsx are allowed to upload' }), 400

@app.route('/sync_recipe',methods=['POST','GET'])
def sync_recipe():
    
    path = session.get('recipe_xlsx')
    print(f"here ->{path}")
    try:
        if os.path.exists(path):
            flag = updateRecipe(FILE_PATH=path)
            if flag:
                saveLogs(log="Recipe uploaded on server")
                os.remove(path)
                print('recipe uploaded on server and xlsx is deleted!!')
                return jsonify({'message':'Recipe uploaded on server successfully', 'timestamp':str(datetime.datetime.now())[:-6], 'error':''})
            else:
                saveLogs(log="Recipe NOT uploaded on server, conn error")
                return jsonify({'message':'Recipe upload unsuccessfull', 'timestamp':str(datetime.datetime.now())[:-6], 'error at server.sync()': '  -> connection to databased failed'})
        else:
            print(f"pathError:Path not found on server, path:{path}")
            return jsonify({'timestamp':str(datetime.datetime.now())[:-6], 'message': '  Error raised at server.sync(): path error, refresh and re-upload the schdule!!' ,'error':'path not exists'})
        
    except Exception as e:
        print(f'filepath : {path}, error at server.sync() :{e}')
        saveLogs(log=f"Recipe not loaded on server, {e}")
        return jsonify({'timestamp':str(datetime.datetime.now())[:-6], 'message': '  Exception raised at server.sync(): refresh and re-upload the schdule!!'  , 'error':str(e)})
    
@app.route('/download_recipe', methods=['GET', 'POST'])
def download_recipe():
    try:
        filename = export_to_excel()
        
        if filename==-1:
            return jsonify({'message':'', 'error': 'File not found'}), 404
        
        filepath =  os.path.join('C:\\Reports', filename)
        
        if not os.path.isfile(filepath):
            return jsonify({'message':'', 'error': 'File not found'}), 404

        print(f'Sending file: {filepath}')
        
        if os.path.exists(filepath):
            return send_file(filepath,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        as_attachment=True,
                        download_name=os.path.basename(filepath))
        else: 
            return jsonify({'message':'Download Failed', 'error': 'File not found ,retry!!'}), 404
    except Exception as e:
        print(f"Error downloading recipe: {e}")
        return jsonify({'message': 'Error downloading recipe: ' + str(e)})
    
@app.route('/delete_server_data', methods=['POST'])
def delete_server_data():
    password = request.json.get('pass')
    if password == app.secret_key:
        try:
            flag= delete_Data()
            if flag==1:
                saveLogs(log="Server DB all table's data deleted!!")
                print("Server DB all table's data deleted!!")
                return jsonify({'message':'Server data deleted Successfully!!','timestamp':str(datetime.datetime.now())[:-6]})
            else:
                saveLogs(log=f"attempt to delete server data failed Error:{flag}")
                return jsonify({'timestamp':str(datetime.datetime.now())[:-6],'message':'Server data NOT deleted ', 'error': flag})
        except Exception as e:
            saveLogs(log="server data delete attempt failed!!")
            return jsonify({'timestamp':str(datetime.datetime.now())[:-6],'message':'Error at deleteData(): data did not deleted!!', 'error':str(e)})
    else:
        saveLogs(log=f"attempt to delete server data failed, Error:Wrong password!")
        return jsonify({'timestamp':str(datetime.datetime.now())[:-6],'message':' Data did NOT deleted!!', 'error':'Wrong password!!'})

@app.route('/get_details', methods=['GET','POST'])
def get_id_details():
    data = request.get_json()
    prod_id = data.get('PROD_ID')
    Dict_obj = getDetails(id=prod_id)
    pprint(Dict_obj)
    return jsonify(Dict_obj)
    

@app.route('/upload_invcuts', methods=['GET','POST'])
def uploadInv():
    if 'file' not in request.files:
        return jsonify ( {'message':'No file part found!',  'timestamp':str(datetime.datetime.now())[:-6], 'error':'File not selected '} )
    file = request.files['file']
    try:
        if file.filename.endswith('.xlsx'):
            #define directory
            target_dir = "inv_cuts"
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            filename = f"{file.filename}"
            file_path = os.path.join(target_dir, filename)
            
            #save file
            file.save(file_path)
            
            print(f'filepath  :{file_path}')
            flag = uploadInvCuts(path=file_path)
            
            if flag:
                saveLogs(log = "Inv Cuts are uploaded on server")
                return jsonify({'message': file_path, 'timestamp':str(datetime.datetime.now())[:-6]}), 200
            else:
                saveLogs(log = "Inv Cuts upload error,uploadInvCuts()  returned a false value")
                return jsonify({'message': 'Inv Cuts Upload failed , recheck file and upload again', 'timestamp':str(datetime.datetime.now())[:-6], 'error':'refer Logs, uploadInvCuts() returned false value'}), 400
        else:
            return jsonify({  'timestamp':str(datetime.datetime.now())[:-6] ,'flag':flag, 'message': 'Wrong FILE', 'error':' only .xlsx are allowed to upload' }), 400
    except Exception as e:
        print(f'exception at API call of uploadInvCuts(), error:{e}')
        return make_response(jsonify({
            'message': 'Internal Server Error', 
            'timestamp': str(datetime.datetime.now())[:-6], 
            'error': str(e)
        }), 500)

@app.route('/add_invcuts', methods =['POST'])
def add_invCuts():
        flag = loadInvCutsToProd()
        print(f'flag {flag}')
        if flag:
            return jsonify({'timestamp':str(datetime.datetime.now())[:-6],
                            'message':'Inventory Cuts added to production successfully!!'})
        else:
            return jsonify({'timestamp':str(datetime.datetime.now())[:-6],
                            'message':'Inventory cuts are not added!! Retry',
                            'error':''})

@app.route('/upload_manual_cuts', methods=['POST'])
def upload_manual_cuts():
    pass

@app.route('/sync_manual_cuts', methods=['POST'])
def sync_manual_cuts():
    pass

@app.route('/download_report', methods=['POST'])
def download_report():
    data = request.get_json()

    try:
        filename = downloadCutReport(date_from= data['date_from'], date_to=data['date_to'])
        
        if filename==-1:
            return jsonify({'message':'', 'error': 'File not found'}), 404
                
        if not os.path.isfile(filename):
            return jsonify({'message':'', 'error': 'File not found'}), 404

        print(f'Sending file: {filename}')
        
        if os.path.exists(filename):
            return send_file(filename,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        as_attachment=True,
                        download_name=os.path.basename(filename))
        else: 
            return jsonify({'message':'Download Failed 5896', 'error': 'File not found ,retry!!'}), 404
    except Exception as e:
        print(f"Error downloading recipe: {e}")
        return jsonify({'message': 'Error downloading recipe: ' + str(e)})
    


if __name__ == '__main__':
    app.run(host='192.168.1.38', port=9600, debug=True)
