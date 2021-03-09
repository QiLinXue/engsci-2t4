class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.connections = []
        self.visited = False
        self.x = x
        self.y = y
        self.distance = 999999

def connect(node1, node2, weight):
    node1.connections.append({"node": node2, "weight": weight})
    node2.connections.append({"node": node1, "weight": weight})

A = Node("A", 0, 0)
B = Node("B", 1, 0)
C = Node("C", 2, -1)
D = Node("D", 1, -1)
E = Node("E", 0, -1)
F = Node("F", 0, -2)

connect(A,B,1); connect(E,F,1); connect(E,D,1)
connect(B,D,1); connect(D,C,1); connect(B,C,3); connect(B,E,1.4)

def h(con):
    v = con["node"]
    return abs(v.x)+abs(v.y)

def greedy(source, dest):

    v = source
    S = [] # Visited Nodes
    d = {v.name: 0}

    # Continue until destination is reached
    while not v == dest:

        con = sorted(v.connections, key=h)[0]
        con["node"].distance = v.distance + con["weight"]
        d[con["node"].name] = con["weight"] + d[v.name]

        v = con["node"]

        S.append(v)

    return d

print(greedy(C, A)) # {'C': 0, 'B': 1.4, 'A': 2.4}