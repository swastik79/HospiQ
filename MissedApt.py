import csv

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
    def printlist(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next
def read_csv(file_name):
    linked_list = LinkedList()
    with open(file_name, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            linked_list.append(row)
    return linked_list

counter1 = read_csv('Counter1.txt')
counter1.printlist()

counter2 = read_csv('Counter2.txt')
counter2.printlist()

counter3 = read_csv('Counter3.txt')
counter3.printlist()

mq = 1
mq_dict = {}

if mq in counter1:
    counter1.remove(mq)
    mq_dict[mq] = "Counter 1"
elif mq in counter2:
    counter2.remove(mq)
    mq_dict[mq] = "Counter 2"
elif mq in counter3:
    counter3.remove(mq)
    mq_dict[mq] = "Counter 3"
else:
    print("This queue number does not exist")

# Open the CSV file for writing
with open('numbers.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the number to a row in the CSV file
    writer.writerow([mq_dict])


