class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.visited = False


def connect(node1, node2, weight):
    node1.connections.append({"node": node2, "weight": weight})
    node2.connections.append({"node": node1, "weight": weight})

A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")

connect(A,B,3)
connect(E,F,8)
connect(B,E,7)
connect(E,D,5)
connect(B,D,1)
connect(B,C,2)
connect(D,C,4)

def get_all_nodes(node):
    connections = []

    q = [node]
    node.visited = True
    while len(q) > 0:
        cur = q.pop(0) # remove q[0] from q and put it in cur
        connections.append(cur)
        for con in cur.connections:
            if not con["node"].visited:
                q.append(con["node"])
                con["node"].visited = True
    
    return connections

def dijsktra(node):

    S = [node] # Visited Nodes
    d = {node.name: 0} # Dictionary of distances to nodes
    prev = {}

    unexplored = get_all_nodes(node) # Unexplored nodes (S + unexplored = all nodes)

    # Set all nodes to infinity
    for n in unexplored:
        if n.name not in d:
            d[n.name] = 999999

    # Continue until everything is explored
    while len(unexplored) > 0:
        cur = unexplored.pop(0)
        for con in cur.connections:
            if con["node"] not in S:
                if con["weight"] + d[cur.name] < d[con["node"].name]:
                    d[con["node"].name] = con["weight"] + d[cur.name]

        S.append(cur)

    return d

print(dijsktra(C)) # {'C': 0, 'B': 2, 'D': 3, 'A': 5, 'E': 8, 'F': 16}

print()

import heapq

class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.visited = False
        self.distance = 999999

    def __lt__(self, other):
        # Comparison function for priority queue
        return self.distance < other.distance

A = Node("A"); B = Node("B"); C = Node("C"); D = Node("D"); E = Node("E"); F = Node("F")

connect(A,B,3); connect(E,F,8); connect(B,E,7); connect(E,D,5)
connect(B,D,1); connect(B,C,2); connect(D,C,4)

def dijsktra_pq(node):
    node.distance = 0

    S = [] # Visited Nodes    
    pq = [node]
    heapq.heapify(pq)

    d = {node.name: 0} # Dictionary of distances to nodes

    # Continue until everything is explored
    while len(pq) > 0:
        cur = heapq.heappop(pq)

        if cur in S:
            continue
        
        d[cur.name] = cur.distance

        for con in cur.connections:
            con["node"].distance =  cur.distance + con["weight"]
            heapq.heappush(pq, con["node"]) 

        S.append(cur)

    return d

print(dijsktra_pq(C)) # {'C': 0, 'B': 2, 'D': 3, 'A': 5, 'E': 8, 'F': 16}