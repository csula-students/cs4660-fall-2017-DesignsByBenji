"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs

# import queue for Python 2 and 3
try:
    import Queue as queue
except ImportError:
    import queue

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
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def bfs(initial_node, dest_node, health=0):
    results = []
    parents = {}
    distances = {initial_node : 0}
    path = {}
    the_queue = queue.Queue()
    the_queue.put(initial_node)

    while the_queue:
        current = the_queue.get()
        neighbors = get_state(current)['neighbors']
        if current == dest_node:
            temp = current
            while temp in parents:
                results.append(path[temp])
                temp = parents[temp]
            results.reverse()
            for result in results:
                node = get_state(initial_node)
                next = result['id']
                initial_name = node['location']['name']
                dest_name = result['action']
                health += result['event']['effect']
                print(initial_name + "(" + initial_node + "):" + dest_name  + "(" + result['id'] + "):" + str(result['event']['effect']))
                initial_node = next
            print("Health Differential: " + str(health))
            return
        for neighbor in neighbors:
            neighbor = neighbor['id']
            if neighbor not in distances:
                distances[neighbor] = distances[current]+1
                parents[neighbor] = current
                path[neighbor] = transition_state(current, neighbor)
                the_queue.put(neighbor)

def djikstra(initial_node, dest_node, health=0):
    results = []
    parents = {}
    distances = {initial_node : 0}
    path = {}
    explored = []
    the_queue = queue.PriorityQueue()
    the_queue.put((0, initial_node))

    while the_queue:
        current = the_queue.get()[1]
        explored.append(current)
        neighbors = get_state(current)['neighbors']
        if current == dest_node:
            temp = dest_node
            while temp in parents:
                results.append(path[temp])
                temp = parents[temp]
            results.reverse()
            for result in results:
                node = get_state(initial_node)
                next = result['id']
                initial_name = node['location']['name']
                dest_name = result['action']
                health += result['event']['effect']
                print(initial_name + "(" + initial_node + "):" + dest_name  + "(" + result['id'] + "):" + str(result['event']['effect']))
                initial_node = next
            print("Health Differential: " + str(health))
            return
        for neighbor in neighbors:
            neighbor = neighbor['id']
            edge = transition_state(current, neighbor)
            distance = distances[current] - edge['event']['effect']
            if (neighbor not in distances or distance < distances[neighbor]) and neighbor not in explored:
                if neighbor in distances:
                    the_queue.get(neighbor)
                distances[neighbor] = distance
                parents[neighbor] = current
                path[neighbor] = edge
                the_queue.put((distances[neighbor],neighbor))

if __name__ == "__main__":
    # Your code starts here
    start = '7f3dc077574c013d98b2de8f735058b4'
    destination = 'f1f131f647621a4be7c71292e79613f9'
print('Breadth First Search:')
bfs(start, destination)
print('\nDjikstra Search:')
djikstra(start, destination)
