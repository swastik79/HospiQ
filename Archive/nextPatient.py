import csv
from flask import Flask, Response, jsonify, request, make_response
from flask_cors import CORS
import os


class Node:
    def __init__(self, data, data1):
        self.data = data  # queue no are stored in data
        self.data1 = data1  # email ids are stored in data1
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data[0], data[1])
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
            l.append(current.data)  # change to data1 to show email ids
            current = current.next
        return l

    def enqueue(self, data):
        if self.last is None:
            self.head = Node(data)
            self.last = self.head
        else:
            self.last.next = Node(data)
            self.last = self.last.next

    def dequeue(self):
        if self.head is None:
            return None
        else:
            temp = self.head
            val_returned = self.head.data
            self.head = self.head.next
            temp = None
            return val_returned

    def front_num(self):
        if self.head:
            return self.head.data
        else:
            return None


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
# print(counter1.printlist())


counter2 = read_csv('Counters/Counter2.txt')
c2l = counter2.printlist()
# print(counter2.printlist())

counter3 = read_csv('Counters/Counter3.txt')
c3l = counter3.printlist()
# print(counter3.printlist())


counter_missedq = read_csv('Counters/MissedQNo.txt')
cmq = counter_missedq.printlist()
print(counter_missedq.printlist())


def llToFile(ll, file_name):
    current = ll.head
    with open(file_name, 'w') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1)) + '\n')
            current = current.next
    f.close()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# --------------------------------------------------------------------------------------------------------
# this function is triggered from the frontend when the counter staff presses "Call Patient" button.
# the respective counter file is retrieved and the first Q num returned to frontend.
# the first Q num is then dequeued to allow other counters to call the next patient
# in line in the counter file.


@app.route('/Qtype/Outpatient', methods=['GET'])
def call_patient():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    #    avail_files = os.listdir()
    #    c_files = [n for n in avail_files] #generate a list of the existing files

    # change according to counter required
    #    for i in c_files:
    #        if "Counter1" in i:
    #                Q_file = i

    #    counter = read_csv(Q_file)
    counter = read_csv("Counter1.txt")
    num = counter.front_num()

    # put all Q that's already called into another "called_num.txt",
    # so that num inside may be sent to MissedQ later if required
    temp = LinkedList()
    new_node = Node(counter.head.data, counter.head.data1, counter.head.data2)
    temp.head = new_node
    current = temp.head
    # login_id to be updated according to the login_id from frontend
    with open('called_num.txt', 'a') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1) + ',' + "login_id" + '\n'))
            current = current.next
            f.close()

    counter.dequeue()
    llToFile(counter, "Counter1.txt")

    # return the num for display at frontend
    return num


@app.route('/Qtype/Senior', methods=['GET'])
def call_patient():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    #    avail_files = os.listdir()
    #    c_files = [n for n in avail_files] #generate a list of the existing files

    # change according to counter required
    #    for i in c_files:
    #        if "Counter1" in i:
    #                Q_file = i

    #    counter = read_csv(Q_file)
    counter = read_csv("Counter2.txt")
    num = counter.front_num()

    # put all Q that's already called into another "called_num.txt",
    # so that num inside may be sent to MissedQ later if required
    temp = LinkedList()
    new_node = Node(counter.head.data, counter.head.data1, counter.head.data2)
    temp.head = new_node
    current = temp.head
    # login_id to be updated according to the login_id from frontend
    with open('called_num.txt', 'a') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1) + ',' + "login_id" + '\n'))
            current = current.next
            f.close()

    counter.dequeue()
    llToFile(counter, "Counter2.txt")

    # return the num for display at frontend
    return num


@app.route('/Qtype/Lab', methods=['GET'])
def call_patient():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}
    #    avail_files = os.listdir()
    #    c_files = [n for n in avail_files] #generate a list of the existing files

    # change according to counter required
    #    for i in c_files:
    #        if "Counter1" in i:
    #                Q_file = i

    #    counter = read_csv(Q_file)
    counter = read_csv("Counter3.txt")
    num = counter.front_num()

    # put all Q that's already called into another "called_num.txt",
    # so that num inside may be sent to MissedQ later if required
    temp = LinkedList()
    new_node = Node(counter.head.data, counter.head.data1, counter.head.data2)
    temp.head = new_node
    current = temp.head
    # login_id to be updated according to the login_id from frontend
    with open('called_num.txt', 'a') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1) + ',' + "login_id" + '\n'))
            current = current.next
            f.close()

    counter.dequeue()
    llToFile(counter, "Counter3.txt")

    # return the num for display at frontend
    return num


# --------------------------------------------------------------------------------------------------------

# this function is triggered from the frontend when the counter staff presses "Send to Missed Q" button
# the latest Q in the called_num.txt, bearing the counter's login_id, will be retrieved.
# login_id will be removed and the Q now sent to MissedQNo.txt


@app.route('/Qtype/Outpatient/missQ', methods=['GET'])
def counter_to_MissedQ():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}

    # to update 'login_id" and "C1" according to the Qtype.
    with open('called_num.txt', 'r') as f:
        data = f.readlines()
        data1 = [i.replace('\n', "") for i in data if 'login_id' in i]
        num = data1.pop().replace('login_id', "C1")

    # num is the the most recent queue that was called by the counter.
    # send num to the MissedQno.txt
    with open('MissedQNo.txt', 'a') as f:
        f.write(num + '\n')

    # Message to display after "Send to Missed Q" button is pressed.
    return "Sent"


@app.route('/Qtype/Senior/missQ', methods=['GET'])
def counter_to_MissedQ():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}

    # to update 'login_id" and "C1" according to the Qtype.
    with open('called_num.txt', 'r') as f:
        data = f.readlines()
        data1 = [i.replace('\n', "") for i in data if 'login_id' in i]
        num = data1.pop().replace('login_id', "C2")

    # num is the the most recent queue that was called by the counter.
    # send num to the MissedQno.txt
    with open('MissedQNo.txt', 'a') as f:
        f.write(num + '\n')

    # Message to display after "Send to Missed Q" button is pressed.
    return "Sent"


@app.route('/Qtype/Lab/missQ', methods=['GET'])
def counter_to_MissedQ():
    headers = {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET,POST,PATCH,OPTIONS',
               'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token'}

    # to update 'login_id" and "C1" according to the Qtype.
    with open('called_num.txt', 'r') as f:
        data = f.readlines()
        data1 = [i.replace('\n', "") for i in data if 'login_id' in i]
        num = data1.pop().replace('login_id', "C3")

    # num is the the most recent queue that was called by the counter.
    # send num to the MissedQno.txt
    with open('MissedQNo.txt', 'a') as f:
        f.write(num + '\n')

    # Message to display after "Send to Missed Q" button is pressed.
    return "Sent"


# --------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(host='localhost', port=9001, debug=False)
