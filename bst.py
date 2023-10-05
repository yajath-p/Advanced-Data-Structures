import json
from typing import List

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    if root is None:
        root = Node(key=key, keycount=1)
        return root
        
    if root.key == key:
        root.keycount +=1

    elif key < root.key:
        root.leftchild = insert(root.leftchild, key)
    
    elif key > root.key:
        root.rightchild = insert(root.rightchild, key)

    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    if root is None:
        return root
    if key < root.key:
        root.leftchild = delete(root.leftchild, key)
        return root
    if key > root.key:
        root.rightchild = delete(root.rightchild, key)
        return root

    if root.keycount >= 1:
            root.keycount -= 1
        
    if root.keycount == 0:
        if root.leftchild is None and root.rightchild is None:
            return None
        if root.leftchild is None:
            return root.rightchild
        elif root.rightchild is None:
            return root.leftchild
        else:
            inorder_successor = minNode(root.rightchild)
            root.key = inorder_successor.key
            root.keycount = inorder_successor.keycount
            for x in range(inorder_successor.keycount):
                root.rightchild = delete(root.rightchild, inorder_successor.key)
    return root

def minNode(node: Node) -> Node:
    curr = node
    while curr.leftchild is not None:
        curr = curr.leftchild
    return curr

# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    list = search_helper(root,search_key)
    return json.dumps(list,indent=2)

def search_helper(root: Node, search_key: int) -> list:
    nodes = []

    if root is None:
        return nodes
    
    nodes.append(root.key)

    if root.key == search_key:
        return nodes
    
    if root.key < search_key:
        nodes += search_helper(root.rightchild, search_key)
        
    if root.key > search_key:
        nodes += search_helper(root.leftchild, search_key)

    return nodes

    
    

# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorder(root: Node) -> str:
    list = preorder_helper(root)
    return json.dumps(list, indent=2)

def preorder_helper(root: Node) -> list:
    if root is None:
        return [] 
    list = []
    list.append(root.key)
    list += preorder_helper(root.leftchild)
    list += preorder_helper(root.rightchild)
    return list
    

# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorder(root: Node) -> str:
    list = inorder_helper(root)
    return json.dumps(list, indent=2)

def inorder_helper(root: Node) -> list:
    if root is None:
        return [] 
    list = []
    list += inorder_helper(root.leftchild)
    list.append(root.key)
    list += inorder_helper(root.rightchild)
    return list

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.
def postorder(root: Node) -> str:
    list = postorder_helper(root)
    return json.dumps(list, indent=2)

def postorder_helper(root: Node) -> str:
    if root is None:
        return [] 
    list = []
    list += postorder_helper(root.leftchild)
    list += postorder_helper(root.rightchild)
    list.append(root.key)

    return list

# For the tree rooted at root, find the BFT traversal (go left-to-right).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    if root is None:
        return []  

    result = []
    queue = []
    current_node = root
    queue.append(current_node)
    
    while queue:
        current_node = queue.pop(0)
        result.append(current_node.key)
        if current_node.leftchild is not None:
            queue.append(current_node.leftchild)
        if current_node.rightchild is not None:
            queue.append(current_node.rightchild)
        
    return json.dumps(result, indent=2)