# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:35:17 2023

@author: pc
"""
import FreeSimpleGUI as sg


class TreeData(sg.TreeData):

    def __init__(self):
        super().__init__()

    def move(self, key1, key2):
        if key1 == '':
            return False
        node = self.tree_dict[key1]
        parent1_node = self.tree_dict[node.parent]
        parent1_node.children.remove(node)
        parent2_node = self.tree_dict[key2]
        parent2_node.children.append(node)
        return True

    def delete(self, key):
        if key == '':
            return False
        node = self.tree_dict[key]
        key_list = [key, ]
        parent_node = self.tree_dict[node.parent]
        parent_node.children.remove(node)
        while key_list != []:
            temp = []
            for item in key_list:
                temp += self.tree_dict[item].children
                del self.tree_dict[item]
            key_list = temp
        return True
    
    def delete_tree(self):
        for k in self.tree_dict.keys():
            node = self.tree_dict[k]
            parent_node = self.tree_dict[node.parent]
            if node in parent_node.children:
                parent_node.children.remove(node)
                
    
def Tree(treedata, headings, auto_size_cols, num_rows, col0_width, key, font, row_height, show_expanded, expand_x, expand_y, enable_events, menu):

    return sg.Tree(
        data=treedata,
        headings=headings,
        auto_size_columns=auto_size_cols,
        num_rows=num_rows,
        col0_width=col0_width,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        key=key,
        font=font,
        show_expanded=show_expanded,
        expand_x=expand_x,
        expand_y=expand_y,
        enable_events=enable_events,
        row_height=row_height,
        pad=(0, 0),
        right_click_menu=menu)