import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#PERSONAL HELPER FUNCTIONS
def height(root: Node) -> int:
    if(root is None):
        return 0
    return max(height(root.leftchild), height(root.rightchild)) + 1

def AVL_balance(root: Node) -> int:
    if(root is None):
        return 0
    return height(root.leftchild) - height(root.rightchild)

def right_rotate(root:Node) -> Node:
    left_child = root.leftchild
    tree = left_child.rightchild
    
    left_child.rightchild = root
    root.leftchild = tree

    return left_child

def left_rotate(root:Node) -> Node:
    right_child = root.rightchild
    tree = right_child.leftchild
    
    right_child.leftchild = root
    root.rightchild = tree
    return right_child

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    if(root is None):
        root = Node(key, word, None, None)
    if(key < root.key):
        root.leftchild = insert(root.leftchild, key, word)
    elif(key > root.key):
        root.rightchild = insert(root.rightchild, key, word)

    balance = AVL_balance(root)
    #LL
    if(balance > 1 and key < root.leftchild.key):
        return right_rotate(root)
    #RR
    if(balance < -1 and key > root.rightchild.key):
        return left_rotate(root)
    #RL
    if(balance < -1 and key < root.rightchild.key):
        root.rightchild = right_rotate(root.rightchild)
        return left_rotate(root)
    #LR
    if(balance > 1 and key > root.leftchild.key):
        root.leftchild = left_rotate(root.leftchild)
        return right_rotate(root)
    
    return root


# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    new_root = None
    for [key, word] in items:
        root = bst_insert(root, int(key), word)
    new_root = rebuild_avl_tree(root)
    return new_root

def rebuild_avl_tree(root: Node) -> Node:
    if root is None:
        return None
    nodes = []
    preorder_traversal(root, nodes)
    new_root = None
    for key, word in nodes:
        new_root = insert(new_root, key, word)
    return new_root

def preorder_traversal(root: Node, nodes: List) -> None:
    if root is None:
        return
    nodes.append([root.key, root.word])
    preorder_traversal(root.leftchild, nodes)
    preorder_traversal(root.rightchild, nodes)
    
def bst_insert(root: Node, key: int, word: str) -> Node:
    if(root is None):
        root = Node(key, word, None, None)
    if(key < root.key):
        root.leftchild = bst_insert(root.leftchild, key, word)
    elif(key > root.key):
        root.rightchild = bst_insert(root.rightchild, key, word)
    return root




# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    new_root = None
    new_root = preorder_insert(root, keys, new_root)
    
    return new_root

def preorder_insert(node, keys_to_delete, new_root):
        if node is None:
            return new_root
        if node.key not in keys_to_delete:
            new_root = insert(new_root, node.key, node.word)
        new_root = preorder_insert(node.leftchild, keys_to_delete, new_root)
        new_root = preorder_insert(node.rightchild, keys_to_delete, new_root)
        return new_root
# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    answer_list = search_helper(root, search_key)
    return json.dumps(answer_list,indent=2)

def search_helper(root: Node, search_key: int) -> list:
    if(root is None):
        return None
    answer = []
    answer.append(root.key)

    if(search_key == root.key):
        answer.append(root.word)
    elif(search_key < root.key):
       answer += search_helper(root.leftchild, search_key)
    elif(search_key > root.key):
       answer += search_helper(root.rightchild, search_key)

    return answer

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> Node:
    if(search_key == root.key):
        root.word = replacement_word
        return root
    elif(search_key < root.key):
        replace(root.leftchild, search_key, replacement_word)
    elif(search_key > root.key):
        replace(root.rightchild, search_key, replacement_word)
    
    return root