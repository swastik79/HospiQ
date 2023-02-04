import csv
from flask import Flask, Response, jsonify, request, make_response
from flask_cors import CORS

#Hashmap that save the code for each counter in each branch
queue_code = {'Jurong/Outpatient.txt' : 'jo', 'Jurong/Priority.txt' : 'jp', 'Jurong/Laboratory.txt' : 'jl', 'Changi/Outpatient.txt' : 'co', 'Changi/Priority.txt' : 'cp', 'Changi/Laboratory.txt' : 'cl', 'Yishun/Outpatient.txt' : 'yo', 'Yishun/Priority.txt' : 'yp', 'Yishun/Laboratory.txt' : 'yl'}

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
    queue_no = generateQNo(path)
    with open(path, 'a') as f:
            f.write((str(queue_no) + ',' + str(email)) + '\n')
    f.close()
    return make_response(jsonify({"status": "success", "message": f"Your Queue number is {queue_no}"}), 200, headers)


def generateQNo(path): #
    ql = []
    data = []
    with open(path,"r") as file:
        for line in file:
            data.append(line[:-1])

    print(data)

    for line in data:
        print(line)
        value = line.split(',')
        print(value)
        value = int(value[0][2:])
        ql.append(value)
    if len(ql) != 0:
        new_queue_no = queue_code[path] + str(max(ql) + 1)
    else:
        new_queue_no = queue_code[path] + "1"
    return new_queue_no

if __name__ == '__main__':
    app.run(host = 'localhost',port = 8001,debug = False)




