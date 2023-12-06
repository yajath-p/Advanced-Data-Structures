from __future__ import annotations
import json
import math
from typing import List

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        if self.root is None:
            self.root = NodeLeaf([Datum(point, code)])
            return
    
        parent = None
        curr = self.root
        
        while type(curr) is not NodeLeaf:
            parent = curr
        
            if point[curr.splitindex] < curr.splitvalue:
                curr = curr.leftchild
            else:
                curr = curr.rightchild
                
        curr.data.append(Datum(point, code))
        
        if self.m < len(curr.data):
            max_spreads_list = []
            for i in range(self.k):
                values = [datum.coords[i] for datum in curr.data]
                spread = max(values) - min(values)
                max_spreads_list.append((i, spread))
                
            def custom_sort(item):
                return (-item[1], item[0])

            max_spreads_list.sort(key = custom_sort)
            
            curr.splitindex = max_spreads_list[0][0]
            
            def custom_key(item):
                return [item.coords[i] for i, _ in max_spreads_list]

            curr.data.sort(key=custom_key)
            
            left = curr.data[0:int((self.m + 1) / 2)]
            right = curr.data[int((self.m + 1) / 2):len(curr.data)]
            
            if len(curr.data) % 2 != 1:
                curr.splitvalue = float((curr.data[int((self.m + 1) / 2)-1].coords[curr.splitindex] + curr.data[int((self.m + 1) / 2)].coords[curr.splitindex]) / 2)
            else:
                curr.splitvalue = float(curr.data[int((self.m + 1) / 2)].coords[curr.splitindex])

            split = NodeInternal(curr.splitindex, curr.splitvalue, NodeLeaf(left), NodeLeaf(right))
            
            if parent is None:
                self.root = split
                return
            
            if curr == parent.leftchild:
                parent.leftchild = split
                return
            
            parent.rightchild = split

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        grandparent = None
        parent = None
        curr = self.root
        
        while type(curr) is not NodeLeaf:
            grandparent = parent
            parent = curr
            
            if point[curr.splitindex] < curr.splitvalue:
                curr = curr.leftchild
            else:
                curr = curr.rightchild
                
        loc = 0
        i=0
        while (i < len(curr.data)): 
            if curr.data[i].coords == point:
                loc = i
                break
            i+=1
               
        curr.data.pop(loc)
        
        if len(curr.data) <= 0:
            if parent is None:
                self.root = None
                return
            
            if grandparent is None:
                if curr == parent.rightchild:
                    self.root = parent.leftchild
                else:
                    self.root = parent.rightchild
                return
            
            if parent != grandparent.leftchild:
                if curr != parent.leftchild:
                    grandparent.rightchild = parent.leftchild
                else:
                    grandparent.rightchild = parent.rightchild
            else:
                if curr != parent.leftchild:
                    grandparent.leftchild = parent.leftchild
                else:
                    grandparent.leftchild = parent.rightchild

    def boundingbox(self, node, boundingbox):
        if node is None:
            return
        
        if type(node) is not NodeLeaf:
            self.boundingbox(node.leftchild, boundingbox)
            self.boundingbox(node.rightchild, boundingbox)
            
        else:
            for point in node.data:
                for i in range(self.k):
                    boundingbox[i][1] = max(boundingbox[i][1], point.coords[i])
                    boundingbox[i][0] = min(boundingbox[i][0], point.coords[i])
                    
                
    def box_dist(self, x, boundingbox):
        if type(x) is Datum:
            x = x.coords
            
        val = 0
        i = 0
        while i < self.k:
            if x[i] < boundingbox[i][0]:
                val += pow((boundingbox[i][0] - x[i]), 2)
            elif x[i] > boundingbox[i][1]:
                val += pow((x[i] - boundingbox[i][1]), 2)
            i += 1
                
        return val
    
    def points_dist(self, point1, point2):
        if type(point1) is Datum:
            point1 = point1.coords
            
        if type(point2) is Datum:
            point2 = point2.coords
            
        val = 0
        i = 0
        while i < self.k:
            val += pow((point1[i] - point2[i]), 2)
            i += 1
        return val


    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        leaveschecked = 0
        knnlist = []
        
        def knnh(node):
            if type(node) == NodeInternal:
                left_box = [[9999999.99, -9999999.99] for _ in range(self.k)]
                right_box = [[9999999.99, -9999999.99] for _ in range(self.k)]
                
                self.boundingbox(node.leftchild, left_box)
                self.boundingbox(node.rightchild, right_box)
                
                left_dist = -9999
                right_dist = -9999
                max_dist = 9999999.99
                leaves = 0
                
                if knnlist:
                    max_dist = self.points_dist(point, knnlist[-1])
                    
                if node.leftchild is not None:
                    left_dist = self.box_dist(point, left_box)
                    
                if node.rightchild is not None:
                    right_dist = self.box_dist(point, right_box)
                
                if (len(knnlist) < k or right_dist <= max_dist) and left_dist == -9999:
                    leaves += knnh(node.rightchild)
                    
                elif (len(knnlist) < k or left_dist <= max_dist) and right_dist == -9999:
                    leaves += knnh(node.leftchild)
                
                elif (len(knnlist) < k or right_dist <= max_dist) and right_dist < left_dist:
                    leaves += knnh(node.rightchild)
                    max_dist = self.points_dist(point, knnlist[-1])
                    
                    if len(knnlist) < k or left_dist <= max_dist:
                        leaves += knnh(node.leftchild)
                    
                elif (len(knnlist) < k or left_dist <= max_dist) and right_dist >= left_dist:
                    leaves += knnh(node.leftchild)
                    max_dist = self.points_dist(point, knnlist[-1])
                    
                    if len(knnlist) < k or right_dist <= max_dist:
                        leaves += knnh(node.rightchild)
                        
                return leaves
            
            else:
                for datum in node.data:
                    if len(knnlist) >= k:
                        i = 0
                        while i < len(knnlist):
                            comp = knnlist[i]
                            if self.points_dist(datum, point) < self.points_dist(comp, point) or (self.points_dist(datum, point) == self.points_dist(comp, point) and datum.code < comp.code):
                                knnlist.insert(i, datum)
                                knnlist.pop()
                                break
                            i += 1
                    else:
                        knnlist.append(datum)
                        knnlist.sort(key=lambda datum: (self.points_dist(datum, point), datum.code))
                return 1

        leaveschecked = knnh(self.root)
        
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]},indent=2))