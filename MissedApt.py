import csv
from flask import Flask, jsonify, request
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete_node(self, data):
        current = self.head
        if current.data[0] == data:
            self.head = current.next
            current = None
            return

        while current is not None:
            if current.data[0] == data:
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
            l.extend(current.data)
            current = current.next
        return l
def read_csv(file_name):
    linked_list = LinkedList()
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            linked_list.append(row)
    return linked_list

counter1 = read_csv('Counter1.txt')
c1l = counter1.printlist()
#print(counter1.printlist())

counter2 = read_csv('Counter2.txt')
c2l = counter2.printlist()

counter3 = read_csv('Counter3.txt')
c3l = counter3.printlist()



app = Flask(__name__)
@app.route('/missedQueue', methods = ['POST'])
def getMissedQ():
    missed_qno = str(request.json['queue_number'])
    print(missed_qno)
    if missed_qno in c1l or missed_qno in c2l or missed_qno in c3l:
        #enter the code to call the other function here
        deleteMissedQNo(missed_qno)
        return jsonify({"status": "success", "message": "Queue number found"}), 200
    else:
        return jsonify({"status": "error", "message": "Queue number not found"}), 404

def llToFile(ll,file_name):
    current = ll.head
    with open(file_name, 'w') as f:
        while current.next is not None:
            f.write(str(current.data) + ',')
            current = current.next
        f.write(str(current.data))
    f.close()
def deleteMissedQNo(mqn):
    if mqn in c1l:
        current = counter1.head
        while current is not None:
            if current.data[0] == mqn:
                counter1.delete_node(mqn)
                break
            current = current.next
        print(counter1.printlist())
        #llToFile(counter1,"Counter1.txt")
    elif mqn in c2l:
        current = counter2.head
        while current is not None:
            if current.data == mqn:
                counter2.delete_node(mqn)
                break
            current = current.next
        print(counter2.printlist())
        #llToFile(counter2, "Counter2.txt")
    else:
        current = counter3.head
        while current is not None:
            if current.data == mqn:
                counter1.delete_node(mqn)
                break
            current = current.next
        print(counter3.printlist())
        #llToFile(counter3,"Counter3.txt")



if __name__ == '__main__':
    app.run(host = 'localhost',port = 9001,debug = False)

