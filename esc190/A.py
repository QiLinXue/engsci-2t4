import heapq

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.connections = []
        self.visited = False
        self.x = x
        self.y = y
        self.distance = 999999
        self.estimate = abs(self.x) + abs(self.y)

    def __lt__(self, other):
        # Comparison function for priority queue
        return self.estimate < other.estimate

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
connect(B,D,1); connect(D,C,1); connect(B,C,1.4); connect(B,E,1.4)

def h(v1, v2):
    return abs(v1.x - v2.x)+abs(v1.y - v2.y)

def greedy(source, dest):
    source.distance = 0

    S = [] # Visited Nodes
    pq = [source]
    heapq.heapify(pq)

    d = {source.name: 0} # Dictionary of distances to nodes

    # Continue until destination is reached
    while len(pq) > 0:
        cur = heapq.heappop(pq)

        if cur in S:
            continue

        d[cur.name] = cur.distance

        for con in cur.connections:
            con["node"].distance =  cur.distance + con["weight"]
            con["node"].estimate =  h(con["node"], dest) + con["node"].distance
            heapq.heappush(pq, con["node"])

        S.append(cur)

    return d

print(greedy(C, E)) # {'C': 0, 'B': 1.4, 'A': 2.4}