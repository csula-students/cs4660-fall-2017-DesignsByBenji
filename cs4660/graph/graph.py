"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):

    f = open(file_path)
    number_of_nodes = (int)(f.readline())

    for i in range(number_of_nodes):
        graph.add_node(Node(i))

    for line in f:
        line_array = line.strip('\n').split(':')
        graph.add_edge(Edge(Node(int(line_array[0])), Node(int(line_array[1])), int(line_array[2])))
    f.close()
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        for edge in self.adjacency_list[node_1]:
            if edge.to_node == node_2:
                return True
        return False

    def neighbors(self, node):
        results = []
        for edge in self.adjacency_list[node]:
            results.append(edge.to_node)
        return results

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        else: return False

    def remove_node(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for nodes, edges in self.adjacency_list.items():
                    """SINGLE LINE SOLUTION"""
                    self.adjacency_list[nodes] = [edge for edge in edges if edge.to_node != node]
                    """ LONGER SOLUTION
                    newlist = []
                    for edge in edges:
                        if edge.to_node != node:
                            newlist.append(edge)
                    self.adjacency_list[nodes] = newlist
                    """
            return True
        else: return False

    def add_edge(self, edge):
        neighbors = self.adjacency_list[edge.from_node]
        if edge not in neighbors:
            neighbors.append(edge)
            return True
        else: return False

    def remove_edge(self, edge):
        neighbors = self.adjacency_list[edge.from_node]
        if edge in neighbors:
            neighbors.remove(edge)
            return True
        else: return False

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        index1 = self.__get_node_index(node_1)
        index2 = self.__get_node_index(node_2)
        if self.adjacency_matrix[index1][index2] != 0:
            return True
        """
        for edge in self.adjacency_matrix[self.__get_node_index(node_1)]:
            if edge.to_node == node_2:
                return True
        """
        return False

    def neighbors(self, node):
        results = []
        index = 0
        for element in self.adjacency_matrix[self.__get_node_index(node)]:
            if element != 0:
                results.append(self.nodes[index])
            index+=1
        return results

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            totalNodes = len(self.nodes)
            index = self.__get_node_index(node)
            self.adjacency_matrix.append([])
            for element in self.adjacency_matrix:
                size = len(element)
                if size < totalNodes:
                    for i in range(totalNodes-size):
                        element.append(0)
            return True
        else: return False

    def remove_node(self, node):
        if node in self.nodes:
            index = self.__get_node_index(node)
            del self.nodes[index]
            return True
        else: return False
        """
        TODO: remove edges that attach to deleted node
        """
          

    def add_edge(self, edge):
        destination_index = self.__get_node_index(edge.to_node)
        neighbors = self.adjacency_matrix[self.__get_node_index(edge.from_node)]
        if neighbors[destination_index] != edge.weight:
            neighbors[destination_index] = edge.weight
            return True
        else:
            return False
        """
        if edge not in neighbors:
            neighbors.append(edge)
            return True
        else: return False
        """

    def remove_edge(self, edge):
        """
        neighbors = self.adjacency_matrix[self.__get_node_index(edge.from_node)]
        if edge in neighbors:
            neighbors.remove(edge)
            return True
        else: return False
        """
        from_index = self.__get_node_index(edge.from_node)
        to_index = self.__get_node_index(edge.to_node)
        if(self.adjacency_matrix[from_index][to_index] != 0):
            self.adjacency_matrix[from_index][to_index] = 0
            return True
        return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        if node in self.nodes:
            return self.nodes.index(node)

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return True
        return False

    def neighbors(self, node):
        node_array = []
        for edge in self.edges:
            if edge.from_node == node:
                node_array.append(edge.to_node)
        return node_array

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        return False

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for edge in self.edges:
                if edge.from_node == node or edge.to_node == node:
                    self.remove_edge(edge)
            return True
        else: return False

    def add_edge(self, edge):
        if edge not in self.edges:
            self.edges.append(edge);
            return True
        else: return False

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        else: return False

