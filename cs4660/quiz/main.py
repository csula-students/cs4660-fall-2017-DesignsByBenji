"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import Queue as queue
import json
# from search import searches as searchFunc
# from graph import graph as graphFunc
"""
GRAPH AND SEARCH CODE (COULD NOT IMPORT)
"""
def bfs(graph, initial_node, dest_node):
    result = []
    explored = []
    parents = {initial_node: None}
    distances = {initial_node: 0}
    the_queue = queue.Queue()
    the_queue.put(initial_node)

    while the_queue:
        current = the_queue.get()
        if (current == dest_node):
            parent = parents[current]
            while parent is not None:
                distance = distances[current] - distances[parent]
                edge = Edge(parent, current, distance)
                result.append(edge)
                current = parent
                parent = parents[current]
            result.reverse()
            return result

        if current not in explored:
            explored.append(current)
        for node in graph.neighbors(current):
            if node not in explored:
                explored.append(node)
                the_queue.put(node)
                distances[node] = distances[current] + graph.distance(current, node)
                parents[node] = current
    return result.reverse()

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    distances = {initial_node : 0}
    parents = {initial_node : None}
    the_queue = queue.PriorityQueue()
    the_queue.put(initial_node)
    result = []
    explored = []


    for node in graph.neighbors(initial_node):

        distances[node] = graph.distance(initial_node, node)
        print initial_node
        print node
        print distances[node]
        parents[node] = initial_node
        the_queue.put((distances[node], node))

    while the_queue:
        current = the_queue.get()
        current_node = current

        if current_node == dest_node:
            parent = parents[current_node]
            while parent is not None:
                distance = distances[current_node] - distances[parent]
                edge = Edge(parent, current_node, distance)
                result.append(edge)
                current_node = parent
                parent = parents[current_node]
            result.reverse()
            print result
            return result

        if current_node not in explored:
            explored.append(current_node)
        for node in graph.neighbors(current_node):
            if node not in explored:
                explored.append(node)
                the_queue.put(node)
                distances[node] = distances[current_node] + graph.distance(current, node)
                parents[node] = current_node

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

    def distance(self, fromNode, toNode):
        for edge in self.adjacency_list[fromNode]:
            if edge.to_node == toNode:
                return edge.weight
        return False

"""
--------NEW CODE
"""
# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = json.load(urlopen(req, jsondataasbytes))
    return response

if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    current_room = empty_room
    #dest_room = get_state('f1f131f647621a4be7c71292e79613f9')
    dest_room = get_state('82c7359fcfb85833d5e759a56284e7f0')

    #print(empty_room)
    #print(dest_room)
    #print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))

    # INITIALIZE GRAPH
    graph = AdjacencyList()
    graph.add_node(current_room['id'])
    # ADD NODES TO GRAPH
    for nodes in graph.adjacency_list.keys():
        for node in get_state(nodes)['neighbors']:
            graph.add_node(node['id'])
            weight = transition_state(current_room['id'], node['id'])
            edge = Edge(current_room['id'], node['id'], weight['event']['effect'])
            graph.add_edge(edge)

    # PERFORM SEARCH & PRINT RESULTS
    result = bfs(graph, empty_room['id'], dest_room['id'])
    print result

    #result = dijkstra_search(graph, empty_room['id'], dest_room['id'])
    #print result

