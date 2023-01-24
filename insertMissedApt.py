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

counter2 = read_csv('Counter2.txt')
c2l = counter2.printlist()

counter3 = read_csv('Counter3.txt')
c3l = counter3.printlist()
print(counter3.printlist())
