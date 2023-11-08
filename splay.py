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

    def right_rotate(self, root:Node) -> Node:
        left_child = root.leftchild
        tree = left_child.rightchild
        
        left_child.rightchild = root
        root.leftchild = tree
        
        if tree:
            tree.parent = root
        left_child.parent = root.parent
        root.parent = left_child
        
        return left_child

    def left_rotate(self, root:Node) -> Node:
        right_child = root.rightchild
        tree = right_child.leftchild
        
        right_child.leftchild = root
        root.rightchild = tree
        
        if tree:
            tree.parent = root
        right_child.parent = root.parent
        root.parent = right_child
        
        return right_child

    def splay(self, key):
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
        self.splay(self, key)

    # Insert Method 1
    def insert(self,key:int):
        new = Node(key, None, None)
        
        if self.root is None:
            self.root = new
            return
        
        self.splay(self, key)
  
        if key > self.root.key:
            new.rightchild = self.root.rightchild
            if self.root.rightchild:
                self.root.rightchild.parent = new
            
            new.leftchild = self.root
            self.root.parent = new
            
            self.root.leftchild.rightchild = None
        elif key < self.root.key:
            new.leftchild = self.root.leftchild
            if self.root.leftchild:
                self.root.leftchild.parent = new
            
            new.rightchild = self.root
            self.root.parent = new
            
            self.root.rightchild.leftchild = None
            
        self.root = new
        self.root.parent = None

            

    # Delete Method 1
    def delete(self,key:int):
        self.splay(self, key)
        #both children
        if self.root.leftchild is not None and self.root.rightchild is not None:
            new_root = self.root.leftchild
            self.splay(key)
            self.root.rightchild = new_root
            new_root.parent = self.root
            self.root.parent = None
        #left child only    
        elif self.root.leftchild is not None and self.root.rightchild is None:
            self.root = self.root.leftchild
            if self.root.leftchild:
                self.root.leftchild.parent = None
        #right child only
        elif self.root.leftchild is None and self.root.rightchild is not None:
            self.root = self.root.rightchild
            if self.root.rightchild:
                self.root.rightchild.parent = None
        else: #no children
            self.root = None