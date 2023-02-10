import csv
import os
import smtplib
import ssl
from email.message import EmailMessage


from flask import render_template

#Hashmap that save the code for each counter in each branch
queue_code = {'Jurong/Outpatient.txt' : 'jo', 'Jurong/Priority.txt' : 'jp', 'Jurong/Laboratory.txt' : 'jl', 'Changi/Outpatient.txt' : 'co', 'Changi/Priority.txt' : 'cp', 'Changi/Laboratory.txt' : 'cl', 'Yishun/Outpatient.txt' : 'yo', 'Yishun/Priority.txt' : 'yp', 'Yishun/Laboratory.txt' : 'yl'}
#missed_queue_code = {'Jurong/MissedQNo.txt' : 'j', 'Changi/MissedQNo.txt' : 'c', 'Yishun/MissedQNo.txt' : 'y'}
missed_queue_code1 = { 'j' : 'Jurong/MissedQNo.txt' , 'c' : 'Changi/MissedQNo.txt' , 'y' : 'Yishun/MissedQNo.txt' }

class Node:
    def __init__(self, data, data1):
        self.data = data    #queue no are stored in data
        self.data1 = data1 #email ids are stored in data1
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
            l.append(current.data) #change to data1 to show email ids
            current = current.next
        return l

    def dequeue(self):
        if self.head is None:
            return None
        else:
            temp = self.head
            val_returned = self.head.data
            self.head = self.head.next
            temp = None
            return val_returned
def read_csv(file_name):
    linked_list = LinkedList()
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            linked_list.append(row)
    return linked_list

def generateQNo(path):
    ql = []
    data = []
    with open(path,"r") as file:
        for line in file:
            print(line)
            data.append(line[:-1])

    print("The value of data is",data)
    new_queue_no = ""
    if data == ['']:
        new_queue_no = queue_code[path] + "1"
    else:
        for line in data:
            #print(line)
            value = line.split(',')
            print("The value is",value)
            value = int(value[0][2:])
            ql.append(value)
        if len(ql) != 0:
            new_queue_no = queue_code[path] + str(max(ql) + 1)
        else:
            new_queue_no = queue_code[path] + "1"
    print(new_queue_no)
    return new_queue_no

def llToFile(ll,file_name):
    current = ll.head
    with open(file_name, 'w') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1)) + '\n')
            current = current.next
    f.close()

def deleteMissedQNo(mqn,path):
    missedq_info = []
    counter = read_csv(path)
    current = counter.head
    while current is not None:
        if current.data == mqn:
            missedq_info = [current.data, current.data1]
            print(missedq_info)
            counter.delete_node(mqn)
            break
        current = current.next

    llToFile(counter, path)
    missedq_path = path.split('/')[0] + '/' + 'MissedQNo.txt'
    with open(missedq_path, "a") as f:
        f.write(missedq_info[0] + "," + missedq_info[1] + "\n")

    current = counter.head
    i = 0
    while current is not None:
        i += 1
        current = current.next

    if i >= 4:
        current = counter.head
        email = current.next.next.next.data1
        queue_no1 = current.next.next.next.data
        send_email(email, queue_no1)  # sending notification to 3rd Patient in line


def RequeMissedQ(mqn,missedq_path):
    qno = email = ""
    counter_missedq = read_csv(missedq_path)
    current = counter_missedq.head
    while current is not None:
        if current.data == mqn:
            qno = current.data
            email = current.data1
            counter_missedq.delete_node(mqn)  # deleting from missedq linkedlist
            break
        current = current.next
    #llToFile(counter_missedq,missedq_path) #writing ll to missedq.txt file after deleting the missedqno
    counter_path = ""
    for i in queue_code:
        if queue_code[i] == mqn[:2]:
            counter_path = i
            break
    print(counter_path)
    counter = read_csv(counter_path)
    current = counter.head
    if current is None:
        counter.append([qno,email])
    else:
        i = 1
        while i < 4:
            if current.next is None:
                break
            current = current.next
            i += 1
        new_node = Node(qno, email)
        new_node.next = current.next
        current.next = new_node

    llToFile(counter,counter_path)

    current = counter_missedq.head
    with open(missedq_path, 'w') as f:
        while current is not None:
            f.write((str(current.data) + ',' + str(current.data1) + ',' +'\n'))
            current = current.next
    f.close()


def send_email(email,queue_no):
    email_sender = "hospiq079@gmail.com"
    email_password = "iqpqsqjqygrbxryl"

    email_receiver = email
    subject = 'Your Queue Status'
    body = f'{queue_no} is now the 3rd patient in the queue!'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



def displayMyQ(branch):
    counter1 = read_csv(f'{branch}/Outpatient.txt')
    c1l = counter1.printlist()
    if c1l != []:
        displayc1 = c1l[0] #Shows now serving
    else:
        displayc1 = None

    counter2 = read_csv(f'{branch}/Priority.txt')
    c2l = counter2.printlist()
    if c2l != []:
        displayc2 = c2l[0] #Shows now serving
    else:
        displayc2 = None

    counter3 = read_csv(f'{branch}/Laboratory.txt')
    c3l = counter3.printlist()
    if c3l != []:
        displayc3 = c3l[0] #Shows now serving
    else:
        displayc3 = None

    counter_missedq = read_csv(f'{branch}/MissedQNo.txt')
    missedq = counter_missedq.printlist()

    counter1m = []
    counter2m= []
    counter3m = []
    for i in missedq:
        if i[1] == 'o':
            counter1m.append(i)
        elif i[1] == 'p':
            counter2m.append(i)
        else:
            counter3m.append(i)
    print(counter1m)
    print(counter2m)
    print(counter3m)
    counter1missed = ','.join(counter1m)
    counter2missed = ','.join(counter2m)
    counter3missed = ','.join(counter3m)

    queueinline1 = ','.join(c1l[1:])
    queueinline2 = ','.join(c2l[1:])
    queueinline3 = ','.join(c3l[1:])

    if len(c1l) != 0:
        counter1total = (len(c1l) - 1)
    else:
        counter1total = 0
    if len(c2l) != 0:
        counter2total = (len(c2l) - 1)
    else:
        counter2total = 0
    if len(c3l) != 0:
        counter3total = (len(c3l) - 1)
    else:
        counter3total = 0


    return render_template('customer_display.html', name= branch, displayc1=displayc1, counter1missed=counter1missed,
                           displayc2=displayc2, counter2missed=counter2missed,
                           displayc3=displayc3, counter3missed=counter3missed,
                           queueinline1=queueinline1, queueinline2=queueinline2, queueinline3=queueinline3,
                           counter1total=counter1total,
                           counter2total=counter2total, counter3total=counter3total)

