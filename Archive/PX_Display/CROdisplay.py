# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 01:12:01 2023

@author: gohpe
"""

import csv
from flask import Flask, Response, jsonify, request, make_response,render_template, render_template_string
from flask_cors import CORS

app = Flask(__name__)

@app.route('/Q')

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
    
    def printlistcounter(self):
        current = self.head
        counters = []
        while current:
            counters.append(current.data2) #change to data1 to show email ids
            current = current.next
        return counters

def read_csv(file_name):
    linked_list = LinkedList()
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) == 2:
                row.append(None)
            linked_list.append(row)
    return linked_list


counter1J = read_csv('Counter1J.txt')
c1lJ = counter1J.printlist()
displayc1J = c1lJ[0]
#print('counter1 serving:', displayc1)


counter2J = read_csv('Counter2J.txt')
c2lJ = counter2J.printlist()
displayc2J = c2lJ[0]
#print('counter2 serving:', displayc2)


counter3J = read_csv('Counter3J.txt')
c3lJ = counter3J.printlist()
displayc3J = c3lJ[0]
#print('counter3 serving:', displayc3)

counter_missedqJ = read_csv('MissedQJ.txt')
missedqJ = counter_missedqJ.printlist()
#print(missedq)
fromcounterJ = counter_missedqJ.printlistcounter()
#print(fromcounter)
#print(fromcounter[0])
counter1J = []
counter2J = []
counter3J = []
# for i in range (3):
#     print(fromcounter[i])
i=0
while i < len(missedqJ):
    if fromcounterJ[i] == 'c1':
        counter1missJ = missedqJ[i]
        counter1J.append(counter1missJ)
                
    if fromcounterJ[i] == 'c2':
        counter2missJ = missedqJ[i]
        counter2J.append(counter2missJ)
                
    if fromcounterJ[i] == 'c3':
        counter3missJ = missedqJ[i]
        counter3J.append(counter3missJ)
                
    i+=1
    continue
        
# #print('List of missed queue for Counter1:')
# for each in counter1:
#     counter1miss = (each.strip('\n'))
#     #print(counter1miss)
    
# #print('List of missed queue for Counter2:')
# for each2 in counter2:
#     counter2miss = (each2.strip('\n'))
#     #print(counter2miss)
    
# #print('List of missed queue for Counter3:')
# for each3 in counter3:
#     counter3miss = (each3.strip('\n'))
#     #print(counter2miss)

counter1Jmissed = ','.join(counter1J)
counter2Jmissed = ','.join(counter2J)
counter3Jmissed = ','.join(counter3J)

queueinline1J = ','.join(c1lJ[1:])
queueinline2J = ','.join(c2lJ[1:])
queueinline3J = ','.join(c3lJ[1:])

counter1totalJ = (len(c1lJ)-1)
counter2totalJ = (len(c2lJ)-1)
counter3totalJ = (len(c3lJ)-1)

counter1C = read_csv('Counter1C.txt')
c1lC = counter1C.printlist()
displayc1C = c1lC[0]
#print('counter1 serving:', displayc1)


counter2C = read_csv('Counter2C.txt')
c2lC = counter2C.printlist()
displayc2C = c2lC[0]
#print('counter2 serving:', displayc2)


counter3C = read_csv('Counter3C.txt')
c3lC = counter3C.printlist()
displayc3C = c3lC[0]
#print('counter3 serving:', displayc3)

counter_missedqC = read_csv('MissedQC.txt')
missedqC = counter_missedqC.printlist()
#print(missedq)
fromcounterC = counter_missedqC.printlistcounter()
#print(fromcounter)
#print(fromcounter[0])
counter1C = []
counter2C = []
counter3C = []
# for i in range (3):
#     print(fromcounter[i])
i=0
while i < len(missedqC):
    if fromcounterC[i] == 'c1':
        counter1missC = missedqC[i]
        counter1C.append(counter1missC)
                
    if fromcounterC[i] == 'c2':
        counter2missC = missedqC[i]
        counter2C.append(counter2missC)
                
    if fromcounterC[i] == 'c3':
        counter3missC = missedqC[i]
        counter3C.append(counter3missC)
                
    i+=1
    continue
        
counter1Cmissed = ','.join(counter1C)
counter2Cmissed = ','.join(counter2C)
counter3Cmissed = ','.join(counter3C)

queueinline1C = ','.join(c1lC[1:])
queueinline2C = ','.join(c2lC[1:])
queueinline3C = ','.join(c3lC[1:])

counter1totalC = (len(c1lC)-1)
counter2totalC = (len(c2lC)-1)
counter3totalC = (len(c3lC)-1)


counter1Y = read_csv('Counter1Y.txt')
c1lY = counter1Y.printlist()
displayc1Y = c1lY[0]
#print('counter1 serving:', displayc1)


counter2Y = read_csv('Counter2Y.txt')
c2lY = counter2Y.printlist()
displayc2Y = c2lY[0]
#print('counter2 serving:', displayc2)


counter3Y = read_csv('Counter3Y.txt')
c3lY = counter3Y.printlist()
displayc3Y = c3lY[0]
#print('counter3 serving:', displayc3)

counter_missedqY = read_csv('MissedQY.txt')
missedqY = counter_missedqY.printlist()
#print(missedq)
fromcounterY = counter_missedqY.printlistcounter()
#print(fromcounter)
#print(fromcounter[0])
counter1Y = []
counter2Y = []
counter3Y = []
# for i in range (3):
#     print(fromcounter[i])
i=0
while i < len(missedqY):
    if fromcounterY[i] == 'c1':
        counter1missY = missedqY[i]
        counter1Y.append(counter1missY)
                
    if fromcounterY[i] == 'c2':
        counter2missY = missedqY[i]
        counter2Y.append(counter2missY)
                
    if fromcounterY[i] == 'c3':
        counter3missY = missedqY[i]
        counter3Y.append(counter3missY)
                
    i+=1
    continue
        
counter1Ymissed = ','.join(counter1Y)
counter2Ymissed = ','.join(counter2Y)
counter3Ymissed = ','.join(counter3Y)

#queueinline1Y = ','.join(c1lY[1:])
#queueinline2Y = ','.join(c2lY[1:])
#queueinline3Y = ','.join(c3lY[1:])

counter1totalY = (len(c1lY)-1)
counter2totalY = (len(c2lY)-1)
counter3totalY = (len(c3lY)-1)

@app.route('/CROQdisplay/<name>')
def display(name):
    if name == "Jurong":
        return render_template('CRO_display.html',name=name, displayc1=displayc1J,counter1missed=counter1Jmissed, 
                           displayc2=displayc2J,counter2missed=counter2Jmissed,
                           displayc3=displayc3J,counter3missed=counter3Jmissed,
                           counter1total = counter1totalJ,
                           counter2total = counter2totalJ,counter3total = counter3totalJ)
    if name == "Changi":
        return render_template('CRO_display.html',name=name, displayc1=displayc1C,counter1missed=counter1Cmissed, 
                           displayc2=displayc2C,counter2missed=counter2Cmissed,
                           displayc3=displayc3C,counter3missed=counter3Cmissed,
                           counter1total = counter1totalC,
                           counter2total = counter2totalC,counter3total = counter3totalC)
    
    if name == "Yishun":
        return render_template('CRO_display.html',name=name, displayc1=displayc1Y,counter1missed=counter1Ymissed, 
                           displayc2=displayc2Y,counter2missed=counter2Ymissed,
                           displayc3=displayc3Y,counter3missed=counter3Ymissed,
                           counter1total = counter1totalY,
                           counter2total = counter2totalY,counter3total = counter3totalY)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=False)
