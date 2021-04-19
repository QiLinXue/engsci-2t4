class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

if 1:                   A = Node(1)
#                      /           \
if 1:      B = Node(2);             C = Node(3)
#         /       \                 /          \
D = Node(4);     E = Node(5);  F = Node(6);     G = Node(7)

A.left = B; A.right = C
B.left = D; B.right = E
C.left = F; C.right = G

def pre_visualize(root):
    print(root.data)
    for node in [root.left, root.right]:
        if node is not None:
            pre_visualize(node)
pre_visualize(A)

print()

def post_visualize(root):
    for node in [root.left, root.right]:
        if node is not None:
            post_visualize(node)
    print(root.data)
post_visualize(A)

print()

def inorder_visualize(node):
    if node.left is not None:
        inorder_visualize(node.left)
    print(node.data)
    if node.right is not None:
        inorder_visualize(node.right)

inorder_visualize(A)

print() # New Definitions

if 1:                   B = Node(2)
#                      /           \
if 1:           A = Node(1);     D = Node(4)
#                               /          \
if 1:                     C = Node(3);   F = Node(6)
#                                        /         \
if 1:                           E = Node(5);     G = Node(7)

B.left = A; B.right = D
D.left = C; D.right = F 
F.left = E; F.right = G

def search_BST(node, value):
    if node == None: return None # Not Found
    if value == node.data: return node # Found
    if value < node.data: return search_BST(node.left, value) # Search Left
    if value > node.data: return search_BST(node.right, value) # Search Right

print()

def insert_BST(node, value):
    if value < node.data:
        if node.left == None:
            node.left = Node(value)
        else:
            insert_BST(node.left, value)

    if value > node.data:
        if node.right == None:
            node.right = Node(value)
        else:
            insert_BST(node.right, value)

insert_BST(B, 0)

print()

def successor_BST(node):
    cur_node = node.right
    while cur_node.left is not None:
        cur_node = cur_node.left
    return cur_node

print(successor_BST(D).data)

print()
