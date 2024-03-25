from __future__ import annotations
import json
import math
from typing import List

# Node Class
# You may make minor modifications.

class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# Scapegoat Tree Class.
# DO NOT MODIFY.
class SGtree():
    def  __init__(self,
                  a    : int  = None,
                  b    : int  = None,
                  m    : int  = None,
                  n    : int  = None,
                  root : Node = None):
        self.m     = 0
        self.n     = 0
        self.a     = a
        self.b     = b
        self.root  = None

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "k": node.key,
                "v": node.value,
                "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    
    def insert_into_tree(self, key, value):
        alpha = self.b / self.a 
        curr = self.root
        depth = 0

        if curr == None:
            self.root = Node(key, value)

        else:
            prev = None
            new_node = Node(key,value)
            while curr:
                depth += 1
                prev = curr
                if key < curr.key:
                    curr = curr.leftchild
                else:
                    curr = curr.rightchild
            
            if key < prev.key:
                prev.leftchild = new_node
                
            else:
                prev.rightchild = new_node

            new_node.parent = prev
    
        # TODO backtrack / propogate. Check through the tree for scapegaots
        self.n += 1
        if depth > math.log(self.n, self.b / self.a):
            self.trigger_scapegoat_insert(new_node)

    def inorderTraversal(self, root):
        if root is None:
            return []

        if root.leftchild is None and root.rightchild is None:
            return [root]

        left = self.inorderTraversal(root.leftchild)
        root.leftchild = None
        left.append(root)
        left = left + self.inorderTraversal(root.rightchild)
        root.rightchild = None
        root.parent = None
        return left

    
    def restructure(self, root: Node):
    # Remove the next line and fill in code to restructure and assign the newroot.
        root_parent = root.parent
        inorder = self.inorderTraversal(root)
        restructured_tree =  self.restructure_helper(inorder)

        if root_parent == None:
            self.root = restructured_tree
        
        elif root_parent.key > root.key:
            root_parent.leftchild = restructured_tree
        
        else:
            root_parent.rightchild = restructured_tree
        
    def restructure_helper(self, inorder):
        if len(inorder) == 0:
            return None
        center = (len(inorder)) // 2
        newroot = inorder[center]

        if len(inorder) == 1:
            return inorder[0]

        newroot.leftchild = self.restructure_helper(inorder[:center])
        newroot.rightchild = self.restructure_helper(inorder[center+1:])

        if newroot.leftchild:
            newroot.leftchild.parent = newroot
        
        if newroot.rightchild:
            newroot.rightchild.parent = newroot

        return newroot
    
    
    def trigger_scapegoat_insert(self, inserted_node):
        parent = inserted_node.parent
        while parent:
            left_subtree_size = self.get_size(parent.leftchild)
            right_subtree_size = self.get_size(parent.rightchild)
            subtree_size = left_subtree_size + right_subtree_size + 1
            scapegoat_ratio = self.a / self.b

            if (left_subtree_size / subtree_size) > scapegoat_ratio or (right_subtree_size / subtree_size) > scapegoat_ratio:
                self.restructure(parent)
                return

            parent = parent.parent
        return
    
    def get_size(self, root):
        if not root:
            return 0
        
        return 1 + self.get_size(root.leftchild) + self.get_size(root.rightchild)

    def insert(self, key: int, value: str):
        alpha = self.b / self.a
        self.insert_into_tree(key, value)
        # Fill in the details.

    def delete(self, key: int):
        # Fill in the details.
        print(f'Delete: {key}') # This is just here to make the code run, you can delete it.

    def search(self, search_key: int) -> str:
        # Fill in and tweak the return.
            # Remove the next line and fill in code to construct value_list.
        value_list = []
        def getList(root, acc):
            if (root == None):
                return []
            
            if (root.key == search_key):
                return [root.value]

            left = getList(root.leftchild, acc)
            if left:
                left.append(root.value)
                return left
            
            right = getList(root.rightchild, acc)
            if right:
                right.append(root.value)
                return right

            return []
        
        value_list = getList(self.root, [])[::-1]
        return value_list
