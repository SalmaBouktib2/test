from py2neo import Graph, Node, Relationship, NodeMatcher,RelationshipMatcher
import csv
from py2neo.ogm import GraphObject


graph = Graph("bolt://localhost:7687")
node_matcher = NodeMatcher(graph)

def getProdByID(id):
    return node_matcher.match("PRODUCT", id=id).first()

def getUserByName(name):
    return node_matcher.match("USER", fullname=name).first()

def addRelBuy(u,p):
    graph.create(Relationship(u, 'BUY', p))

def addLike(u, p):
    graph.create(Relationship(u, 'LIKE', p))

class User(GraphObject):
    def __init__(self, username):
        self.username = username

    def find(self):
        user = User.match(graph, self.username).first()
        return user

    def register(self, fullname, sexe, birth, password):
        user = Node('USER', username=self.username, password=password, fullname=fullname, sexe=sexe, birth=birth)
        graph.create(user)

    def getUserByName(name):
        return node_matcher.match("USER", username=name).first()


class Product(GraphObject):
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def getAll():
        nodes = list(node_matcher.match("PRODUCT"))
        return nodes

    @staticmethod
    def getAllCasual():
        nodes = list(node_matcher.match("PRODUCT").where(category="casual"))
        return nodes

    @staticmethod
    def getAllSport():
        nodes = list(node_matcher.match("PRODUCT").where(category="sport"))
        return nodes

    @staticmethod
    def getAllFormal():
        nodes = list(node_matcher.match("PRODUCT").where(category="formal"))
        return nodes

    @staticmethod
    def getAllID():
        return graph.run("match (n:PRODUCT) return n.id")

    def getProduct(prod_id):
        node = node_matcher.match("PRODUCT").where(id=prod_id).first()
        return node