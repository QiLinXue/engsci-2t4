class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.visited = False

def connect(node1, node2):
    node1.connections.append(node2)
    node2.connections.append(node1)

A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")

connect(A,B)
connect(E,F)
connect(B,E)
connect(E,D)
connect(B,D)
connect(B,C)
connect(D,C)

def BFS(node):
    q = [node]
    node.visited = True
    while len(q) > 0:
        cur = q.pop(0) # remove q[0] from q and put it in cur
        print(cur.name)
        for con in cur.connections:
            if not con.visited:
                q.append(con)
                con.visited = True

BFS(C) # C B D A E F

def unvisit_all(node):
    '''Change all n.visited to False in all the nodes in the graph of nodes
    connected to node. Use BFS to find all the nodes'''    
    q = [node]
    node.visited = False
    while len(q) > 0:
        cur = q.pop(0) # remove q[0] from q and put it in cur
        for con in cur.connections:
            if con.visited:
                q.append(con)
                con.visited = False
unvisit_all(C)
print()

def DFS(node):
    q = [node]
    node.visited = True
    while len(q) > 0:
        cur = q.pop() # remove last element from q and put it in cur
        print(cur.name)
        for con in cur.connections:
            if not con.visited:
                q.append(con)
                con.visited = True

DFS(C) # C D E F B A

unvisit_all(C)
print()

def DFS_rec(node):
    '''Print out the names of all nodes connected to node using a
    recursive version of DFS'''
    print(node.name)
    node.visited = True
    for con in node.connections:
        if not con.visited:
            DFS_rec(con)

DFS_rec(C) # C B A E F D