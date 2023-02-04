import csv
from flask import Flask, Response, jsonify, request, make_response
from flask_cors import CORS
class Node:
    def __init__(self, data, data1, data2 = None):
        self.data = data    #queue no are stored in data
        self.data1 = data1 #email ids are stored in data1
        self.data2 = data2
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = Node(data[0], data[1], data[2])
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete_node(self, data):
        current = self.head
        if current.data == data:
            self.head = current.next
            current = None
            return

        while current is not None:
            if current.data == data:
                break
            prev = current
            current = current.next

        if current is None:
            return

        prev.next = current.next
        current = None

    def printlist(self):
        current = self.head
        l = []
        while current:
            l.append(current.data) #change to data1 to show email ids
            current = current.next
        return l

def read_csv(file_name):
    linked_list = LinkedList()
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) == 2:
                row.append(None)
            linked_list.append(row)
    return linked_list


counter1 = read_csv('Counters/Counter1.txt')
c1l = counter1.printlist()
#print(counter1.printlist())


counter2 = read_csv('Counters/Counter2.txt')
c2l = counter2.printlist()
#print(counter2.printlist())

counter3 = read_csv('Counters/Counter3.txt')
c3l = counter3.printlist()
#print(counter3.printlist())


counter_missedq = read_csv('Counters/MissedQNo.txt')
cmq = counter_missedq.printlist()
print(counter_missedq.printlist())


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

###########################################################################################################

#This section of code remove patients that missed their appointment from counter to missed queue txt file

@app.route('/missedQueue', methods = ['POST'])
def getMissedQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)

    counter1 = read_csv('Counters/Counter1.txt')
    c1l = counter1.printlist()
    counter2 = read_csv('Counters/Counter2.txt')
    c2l = counter2.printlist()
    counter3 = read_csv('Counters/Counter3.txt')
    c3l = counter3.printlist()

    if missed_qno in c1l or missed_qno in c2l or missed_qno in c3l:
        #enter the code to call the other function here
        deleteMissedQNo(missed_qno)
        return make_response(jsonify({"status": "success", "message": "Queue number found"}), 200, headers)
    else:
        return make_response(jsonify({"status": "error", "message": "Queue number not found"}), 404, headers)

def deleteMissedQNo(mqn):
    missedq_info = []
    if mqn in c1l:
        current = counter1.head
        while current is not None:
            if current.data == mqn:
                missedq_info = [current.data,current.data1,"C1"]
                counter1.delete_node(mqn)
                break
            current = current.next
        #print(counter1.printlist())
        c1l.remove(mqn)
        llToFile(counter1, "Counters/Counter1.txt")
        with open("Counters/MissedQNo.txt", "a") as f:
            f.write(missedq_info[0] + "," + missedq_info[1] + "," + missedq_info[2] + "\n")
    elif mqn in c2l:
        current = counter2.head
        while current is not None:
            if current.data == mqn:
                missedq_info = [current.data, current.data1, "C2"]
                counter2.delete_node(mqn)
                break
            current = current.next
        #print(counter2.printlist())
        c2l.remove(mqn)
        llToFile(counter2, "Counters/Counter2.txt")
        with open("Counters/MissedQNo.txt", "a") as f:
            f.write(missedq_info[0] + "," + missedq_info[1] + "," + missedq_info[2] + "\n")
    else:
        current = counter3.head
        while current is not None:
            if current.data == mqn:
                missedq_info = [current.data, current.data1, "C3"]
                counter3.delete_node(mqn)
                break
            current = current.next
        #print(counter3.printlist())
        c3l.remove(mqn)
        llToFile(counter3, "Counters/Counter3.txt")
        with open("Counters/MissedQNo.txt", "a") as f:
            f.write(missedq_info[0] + "," + missedq_info[1] + "," + missedq_info[2] + "\n")


###########################################################################################################

#This section of code inserts patients from missed queue txt file back to counter


@app.route('/insertQueue', methods = ['POST'])
def insertMissedQ():
    headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,POST,PATCH,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)
    counter_missedq = read_csv('Counters/MissedQNo.txt')
    cmq = counter_missedq.printlist()
    if missed_qno in cmq:
        # enter the code to call the other function here
        RequeMissedQ(missed_qno,counter_missedq,cmq)
        return make_response(jsonify({"status": "success", "message": "Queue number found"}), 200, headers)
    else:
        return make_response(jsonify({"status": "error", "message": "Queue number not found"}), 404, headers)

def llToFile(ll,file_name):
    current = ll.head
    with open(file_name, 'w') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1)) + '\n')
            current = current.next
    f.close()

def RequeMissedQ(mqn, counter_missedq, cmq ):
    current = counter_missedq.head
    qno = email = counter_name = ""

    while current is not None:
        if current.data == mqn:
            qno = current.data
            email = current.data1
            counter_name = current.data2
            counter_missedq.delete_node(mqn) #deleting from missedq linkedlist
            break
        current = current.next

    if counter_name == 'C1':
        current = counter1.head
    elif counter_name == 'C2':
        current = counter2.head
    else:
        current = counter3.head

    i = 1
    while i < 3:
        if current.next is None:
            break
        current = current.next
        i += 1
    new_node = Node(qno, email)
    new_node.next = current.next
    current.next = new_node

    cmq.remove(mqn)
    if counter_name == 'C1':
        llToFile(counter1, "Counters/Counter1.txt")
    elif counter_name == 'C2':
        llToFile(counter2, "Counters/Counter2.txt")
    else:
        llToFile(counter3, "Counters/Counter3.txt")

    #Writing from the updated missed queue linked list to the MissedQ txt file

    current = counter_missedq.head
    with open('Counters/MissedQNo.txt', 'w') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1)+ ',' + str(current.data2)) + '\n')
            current = current.next
    f.close()


if __name__ == '__main__':
    app.run(host = 'localhost',port = 9001,debug = False)
