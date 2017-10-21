"""
Searches module defines all different search algorithms
"""
import Queue as queue
import sys
from graph import graph as graphFunc


def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
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
                edge = graphFunc.Edge(parent, current, distance)
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

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    parents = {}
    dfs_recursive(graph, initial_node, {}, parents)
    path = []
    current_node = dest_node

    while current_node != initial_node:
        next_node = parents[current_node]
        path = [graphFunc.Edge(next_node, current_node, graph.distance(next_node, current_node))] + path
        current_node = next_node
    return path

def dfs_recursive(graph, current, discovered_children, parents):
    for neighbor in graph.neighbors(current):
        if neighbor not in discovered_children:
            discovered_children[neighbor] = True
            parents[neighbor] = current
            dfs_recursive(graph, neighbor, discovered_children, parents)

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    distances = {initial_node : 0}
    parents = {}
    the_queue = queue.PriorityQueue()
    the_queue.put((0,initial_node))
    result = []

    while the_queue:
        current = the_queue.get()[1]
        if current == dest_node:
            temp = dest_node
            #parent = parents[current_node]
            while temp in parents:
                distance = distances[temp]
                edge = graphFunc.Edge(parents[temp], temp, distance)
                result.append(edge)
                temp = parents[temp]
            result.reverse()
            return result
        for node in graph.neighbors(current):
            distance = distances[current] + graph.distance(current, node)
            if node not in distances or distance < distances[node]:
                distances[node] = graph.distance(current, node)
                parents[node] = current
                the_queue.put((distances[node], node))

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass
