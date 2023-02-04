import csv
from flask import Flask, Response, jsonify, request, make_response
from flask_cors import CORS
import Support

#Initializing counters




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
@app.route('/getAppointment', methods = ['POST'])
def getQNo():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    email = str(request.json['email_id'])
    branch = str(request.json['branch_name'])
    patient_type = str(request.json['patient_type'])

    path = f'{branch}/{patient_type}.txt'
    queue_no = Support.generateQNo(path)
    with open(path, 'a') as f:
            f.write((str(queue_no) + ',' + str(email)) + '\n')
    f.close()
    return make_response(jsonify({"status": "success", "message": f"Your Queue number is {queue_no}"}), 200, headers)


#Remove a patient from Counter to MissedQueue file
@app.route('/missedQueue', methods = ['POST'])
def getMissedQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)
    
    for i in Support.queue_code:
        print(Support.queue_code[i])
        if Support.queue_code[i] == missed_qno[:2]:
            Support.deleteMissedQNo(missed_qno,i)
            return make_response(jsonify({"status": "success", "message": "Queue number found"}), 200, headers)

    return make_response(jsonify({"status": "error", "message": "Queue number not found"}), 404, headers)


if __name__ == '__main__':
    app.run(host = 'localhost',port = 9001,debug = False)



