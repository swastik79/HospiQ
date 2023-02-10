import csv
from flask import Flask, Response, jsonify, request, make_response, render_template
from flask_cors import CORS
import Support

start_stop_dict = {'Jurong-Outpatient' : 'start', 'Jurong-Priority' : 'start', 'Jurong-Laboratory' : 'start',
                   'Changi-Outpatient' : 'start', 'Changi-Priority' : 'start', 'Changi-Laboratory' : 'start',
                   'Yishun-Outpatient' : 'start', 'Yishun-Priority' : 'start', 'Yishun-Laboratory' : 'start'}

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

    if start_stop_dict[branch + "-" + patient_type] == 'start':
        path = f'{branch}/{patient_type}.txt'
        queue_no = Support.generateQNo(path)
        with open(path, 'a') as f:
                f.write((str(queue_no) + ',' + str(email)) + '\n')
        f.close()

        counter = Support.read_csv(path)
        current = counter.head
        i = 0
        while current is not None:
            i += 1
            current = current.next

        if i == 4:
            current = counter.head
            email = current.next.next.next.data1
            queue_no1 = current.next.next.next.data
            Support.send_email(email, queue_no1)  # sending notification to 3rd Patient in line

        return make_response(jsonify({"status": "success", "queue_no": queue_no}), 200, headers)
    else:
        return make_response(jsonify({"status": "error", "message": "Queue registration has been stopped for now!"}), 404, headers)


#Remove a patient from Counter to MissedQueue file
@app.route('/missedQueue', methods = ['POST'])
def getMissedQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)
    
    for i in Support.queue_code:
        #print(Support.queue_code[i])
        if Support.queue_code[i] == missed_qno[:2]:
            Support.deleteMissedQNo(missed_qno,i)
            return make_response(jsonify({"status": "success", "message": "Queue number found"}), 200, headers)

    return make_response(jsonify({"status": "error", "message": "Queue number not found"}), 404, headers)



@app.route('/insertQueue', methods = ['POST'])
def insertMissedQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)

    path = Support.missed_queue_code1[missed_qno[0]]
    missed_counter = Support.read_csv(path)
    flag = False
    current = missed_counter.head
    while current:
        if current.data == missed_qno:
            flag = True
        current = current.next

    if flag == True:
        Support.RequeMissedQ(missed_qno, path)
        return make_response(jsonify({"status": "success", "message": "Queue number found"}), 200, headers)
    else:
        return make_response(jsonify({"status": "error", "message": "Queue number not found"}), 404, headers)



@app.route('/nextPatient', methods = ['POST'])
def call_patient():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}

    branch = str(request.json['branch_name'])
    patient_type = str(request.json['patient_type'])
    path = f'{branch}/{patient_type}.txt'
    counter = Support.read_csv(path)
    queue_no = counter.dequeue()
    Support.llToFile(counter, path)

    current = counter.head
    i = 0
    while current is not None:
        i += 1
        current = current.next

    if i >= 4:
        current  = counter.head
        email = current.next.next.next.data1
        queue_no1 = current.next.next.next.data
        Support.send_email(email, queue_no1)  # sending notification to 3rd Patient in line

    if queue_no is not None:
        return make_response(jsonify({"status": "success", "queue_no": queue_no}), 200, headers)
    else:
        return make_response(jsonify({"status": "error", "queue_no": ""}), 404, headers)


@app.route('/Qdisplay/<name>')
def display(name):
    return Support.displayMyQ(name)


@app.route('/QStop', methods = ['POST'])
def StopQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    branch = str(request.json['branch_name'])
    patient_type = str(request.json['patient_type'])

    key = branch + "-" + patient_type
    start_stop_dict[key] = 'stop'
    return make_response(jsonify({"status": "success", "message": "Queue has been stopped!"}), 200, headers)


@app.route('/QStart', methods=['POST'])
def StartQ():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    branch = str(request.json['branch_name'])
    patient_type = str(request.json['patient_type'])

    key = branch + "-" + patient_type
    start_stop_dict[key] = 'start'
    return make_response(jsonify({"status": "success", "message": "Queue has been started again!"}), 200, headers)


if __name__ == '__main__':
    app.run(host = 'localhost',port = 9001,debug = False)




