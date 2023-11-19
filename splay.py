from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)


    def left_rotate(self, root:Node):
        right_child = root.rightchild
        root.rightchild = right_child.leftchild
        
        if right_child.leftchild:
            right_child.leftchild.parent = root
            
        right_child.parent = root.parent
        
        if root.parent is None:
            self.root = right_child
        elif root == root.parent.leftchild:
            root.parent.leftchild = right_child
        else:
            root.parent.rightchild = right_child
            
        right_child.leftchild = root
        root.parent = right_child

    def right_rotate(self, root:Node):
        left_child = root.leftchild
        root.leftchild = left_child.rightchild
        
        if left_child.rightchild:
            left_child.rightchild.parent = root
            
        left_child.parent = root.parent
        
        if root.parent is None:
            self.root = left_child
        elif root == root.parent.leftchild:
            root.parent.leftchild = left_child
        else:
            root.parent.rightchild = left_child
            
        left_child.rightchild = root
        root.parent = left_child
   
    def splay(self, key:int):
        fallout = None
        current = self.root

        while current is not None:
            if key == current.key:
                break
            fallout = current
            if key < current.key:
                current = current.leftchild
            else:
                current = current.rightchild
        else:
            current = fallout

        while current.parent is not None:
            parent = current.parent
            grandparent = parent.parent
            
            if grandparent is None:
                # Zig step
                if current == parent.leftchild:
                    self.right_rotate(parent)
                else:
                    self.left_rotate(parent)
            else:
                if current == parent.leftchild and parent == grandparent.leftchild:
                    #left-left
                    self.right_rotate(grandparent)
                    self.right_rotate(parent)
                elif current == parent.rightchild and parent == grandparent.rightchild:
                    #right-right
                    self.left_rotate(grandparent)
                    self.left_rotate(parent)
                elif current == parent.rightchild and parent == grandparent.leftchild:
                    #left-right
                    self.left_rotate(parent)
                    self.right_rotate(grandparent)
                else:
                    #right-left
                    self.right_rotate(parent)
                    self.left_rotate(grandparent)

        self.root = current

    # Search
    def search(self,key:int):
        self.splay(key)

    # Insert Method 1
    def insert(self,key:int):
        if self.root is None:
            self.root = Node(key)
            return
        
        self.splay(key)

        node_to_add = Node(key)
        
        if key < self.root.key:
            node_to_add.rightchild = self.root
            node_to_add.leftchild = self.root.leftchild
            
            if self.root.leftchild:
                self.root.leftchild.parent = node_to_add
                
            self.root.leftchild = None
        else:
            node_to_add.leftchild = self.root
            node_to_add.rightchild = self.root.rightchild
            
            if self.root.rightchild:
                self.root.rightchild.parent = node_to_add
                
            self.root.rightchild = None
            
        self.root.parent = node_to_add
        self.root = node_to_add

            

    # Delete Method 1
    def delete(self,key:int):
        self.splay(key)
        #both children
        if self.root.leftchild is not None and self.root.rightchild is not None:
            left_subtree = self.root.leftchild
            self.root = self.root.rightchild
            self.splay(key)
            self.root.parent = None
            self.root.leftchild = left_subtree
            left_subtree.parent = self.root
        
        #left child only    
        elif self.root.leftchild is not None and self.root.rightchild is None:
            self.root = self.root.leftchild
            self.root.parent = None
        #right child only
        elif self.root.leftchild is None and self.root.rightchild is not None:
            self.root = self.root.rightchild
            self.root.parent = None
        else: #no children
            self.root = None