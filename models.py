from py2neo import Graph, Node, Relationship
import csv

from py2neo.ogm import GraphObject

#establish the connection
with open("cred.txt") as f1:
    data=csv.reader(f1,delimiter=",")
    for row in data:
        username=row[0]
        pwd=row[1]
        uri=row[2]
print(username,pwd,uri)
graph = Graph("bolt://localhost:7687")

class User(GraphObject):
    def __init__(self, username):
        self.username = username

    def find(self):
        user = User.match(graph, self.username).first()
        return user

    def register(self, password):
        user = Node('User', username=self.username, password=password)
        graph.create(user)