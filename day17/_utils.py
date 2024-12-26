# -*- coding: utf-8 -*-

import numpy as np

# GRAPH and NODE structure

class Graph:
    
    def __init__(self):
        self.nodes = {}
    def add_node(self, node_id, node_props, connection_ids, both_way_connection=True):
        self.nodes[node_id] = Node(node_id, node_props)
        for c_node_id in connection_ids:
            self.nodes[node_id].add_connection(self.nodes[c_node_id])
            if both_way_connection:
                self.nodes[c_node_id].add_connection(self.nodes[node_id])
    def add_connection(self, node1_id, node2_id, both_way_connection=True):
        if self.nodes[node2_id] not in self.nodes[node1_id].connections:
            self.nodes[node1_id].connections.append(self.nodes[node2_id])
        if both_way_connection and self.nodes[node1_id] not in self.nodes[node2_id].connections:
            self.nodes[node2_id].connections.append(self.nodes[node1_id])
    def get_neighbours(self, node_id):
        ids = []
        for n in self.nodes[node_id].connections:
            ids.append(n.id)
        return ids
    def exists_node(self, node_id):
        return node_id in self.nodes.keys()
    def exists_connection(self, node1_id, node2_id):
        return self.nodes[node2_id] in self.nodes[node1_id].connections

class Node:
    
    def __init__(self, id, props):
        self.id = id
        self.properties = props
        self.connections = []
    def add_connection(self, node):
        self.connections.append(node)

def dijkstra(graph, start_node_id, end_node_id, max_dist=1000000, dist_func=lambda n1,n2: 1):
    for node in graph.nodes.values():
        node.properties["distance"] = max_dist
        node.properties["prev"] = None
    graph.nodes[start_node_id].properties["distance"] = 0
    queue = list(graph.nodes.keys())
    while len(queue) != 0:
        queue.sort(key=lambda node_id: graph.nodes[node_id].properties["distance"])
        curr_node_id = queue.pop(0)
        print("Testing", curr_node_id)
        if curr_node_id == end_node_id:
            return graph.nodes[curr_node_id].properties["distance"]
        neighbours = graph.get_neighbours(curr_node_id)
        for n_id in neighbours:
            new_dist = dist_func(curr_node_id, n_id) + graph.nodes[curr_node_id].properties["distance"]
            if new_dist < graph.nodes[n_id].properties["distance"]:
                graph.nodes[n_id].properties["distance"] = new_dist
                graph.nodes[n_id].properties["prev"] = curr_node_id
                

# read lines of txt file and strip \n's
def read_lines(path):
    with open(path) as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i][:-1]
    return lines

def make_matrix_from_readlines(arr):
    res = []
    for line in arr:
        res.append([c for c in line])
    return np.array(res)

# count occurences of numbers in list/array
# arr: array to search; nums: list of numbers whose occurences to count
def count_occurences(arr, nums, already_sorted=False):
    arr = np.array(arr)
    nums = np.array(nums)
    if not already_sorted:
        arr.sort()
        perm = np.argsort(nums)
        inv_perm = np.argsort(perm)
        nums = nums[perm]
    
    i = 0
    occs = []
    for num in nums:
        occ = 0
        while arr[i] < num:
            i += 1
        while arr[i] == num:
            i += 1
            occ += 1
        occs.append(occ)
    
    if already_sorted:
        return np.array(occs)
    return np.array(occs)[inv_perm]

# find substring occurences in a string
# returns indices of occurence
def find_substr(string, substr):
    indices = []
    for i in range(len(string)-len(substr)+1):
        match = True
        for j in range(len(substr)):
            if string[i+j] != substr[j]:
                match = False
                break
        if match:
            indices.append(i)
    return indices

def is_numeric(s):
    s = str(s)
    for c in s:
        if c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return False
    return True

# search all directions from a certain point in a rectangular 2d array for a character
# matrix: 2d array to search through, c: character to search, coords: 1d array of starting coords
# returns directions in which character appears
def search_all_directions(matrix, c, coords):
    dirs = []
    for i in [-1, 0, 1]:
        for j in [-1,0,1]:
            if i != 0 or j != 0:
                if coords[0]+i >= 0 and coords[0]+i < len(matrix) and coords[1]+j >= 0 and coords[1]+j < len(matrix[0]):
                    s = matrix[coords[0]+i][coords[1]+j]
                    if s == c:
                        dirs.append([i,j])
    return dirs

# searches one direction in 2d matrix fro sequence
# matrix: 2d array to search through, chars: char sequence to find, coords: starting point,
# direction: given as e.g. [1,0] for 1 step down, [0,-2] for two steps left, [1,1] diagonal etc
def search_one_direction(matrix, chars, coords, direction):
    coords_c = coords.copy()
    for c in chars:
        coords_c[0] += direction[0]
        coords_c[1] += direction[1]
        if coords_c[0] >= 0 and coords_c[0] < len(matrix) and coords_c[1] >= 0 and coords_c[1] < len(matrix):
            found = c == matrix[coords_c[0]][coords_c[1]]
        else:
            return False
        if not found:
            return False
    return True