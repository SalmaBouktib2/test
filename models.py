from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import csv

from py2neo.ogm import GraphObject

# establish the connection
with open("cred.txt") as f1:
    data = csv.reader(f1, delimiter=",")
    for row in data:
        username = row[0]
        pwd = row[1]
        uri = row[2]
print(username, pwd, uri)
graph = Graph("bolt://localhost:7687")
node_matcher = NodeMatcher(graph)


class User(GraphObject):
    def __init__(self, username):
        self.username = username

    def find(self):
        user = User.match(graph, self.username).first()
        return user

    def getUserByName(name):
        return node_matcher.match("User", username=name).first()

    def registerSlm(self, password):
        user = Node('User', username=self.username, password=password)
        graph.create(user)

    def register(self, fullname, sexe, birth, password):
        user = Node('User', username=self.username, password=password, fullname=fullname, sexe=sexe, birth=birth)
        graph.create(user)

    @staticmethod
    def isLike(user, produit):
        like = Relationship.type("LIKE")
        graph.merge(like(user, produit))


    @staticmethod
    def isDLike(personne, produit):
        dlike = Relationship.type("DONT_LIKE")
        graph.merge(dlike(personne, produit))


class Product(GraphObject):
    def __init__(self):
        pass

    @staticmethod
    def getAll():
        nodes = list(node_matcher.match("PRODUCT"))
        return nodes

    @staticmethod
    def getAllID():
        return graph.run("match (n:PRODUCT) return n.id")
    def getProduct(prod_id):
        node = node_matcher.match("PRODUCT").where(id=prod_id).first()
        return node
