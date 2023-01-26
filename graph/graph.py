from graph.insorts import insort_left

class Graph:
    def __init__(self, nodes_dictionary: dict, graph_id=None):
        self.graph_id = graph_id
        self.nodes = nodes_dictionary
        self.__connectivity = {}

    def __copy__(self, new_id=None):
        g_copy = Graph(self.nodes.copy())
        g_copy.__connectivity = self.__connectivity.copy()
        g_copy.graph_id = new_id

    def add_node(self, key, node):
        self.nodes[key] = node

    def __getitem__(self, key):
        return self.nodes[key]

    def remove_node(self, key):
        self.validate_nodes(key)
        self.nodes.pop(key)
        self.__connectivity.pop(key, None)
        for each_node in self.__connectivity.values():
            each_node.pop(key, None)

    def add_edge(self, from_node, to_node, weight):
        self.validate_nodes(from_node, to_node)
        self.__connectivity.setdefault(from_node, {})
        self.__connectivity[from_node][to_node] = weight

    def remove_edge(self, from_node, to_node):
        if from_node in self.__connectivity and to_node in self.__connectivity[from_node]:
            self.__connectivity[from_node].pop(to_node)
            return True
        else:
            return False

    def get_distance(self, from_node, to_node):
        try:
            return self.__connectivity[from_node][to_node]
        except KeyError:
            return None

    def validate_nodes(self, *node_keys):
        for node_key in node_keys:
            if node_key not in self.nodes:
                raise InvalidNodeKey(node_key)

    def get_neighbouring_keys(self, node_key):
        if node_key not in self.__connectivity:
            return ()
        for neighbour_key, distance in self.__connectivity[node_key].items():
            if distance != float('inf'):
                yield neighbour_key

    def nodes_count(self):
        return len(self.nodes)

    def single_source_shortest_parth(self, start_node):
        self.validate_nodes(start_node)
        pq = PriorityQueue()
        dist = {key: float('inf') for key in self.nodes.keys()}
        pred = {key: None for key in self.nodes.keys()}
        dist[start_node] = 0

        for key, distance in dist.items():
            pq.add_with_priority(key, distance)

        while not pq.is_empty():
            node_key = pq.pop_min()
            for neighbour_key in self.get_neighbouring_keys(node_key):
                d = self.get_distance(node_key, neighbour_key)
                new_dist = dist[node_key] + d
                if new_dist < dist[neighbour_key]:
                    pq.change_priority(item=neighbour_key, new_priority=new_dist)
                    dist[neighbour_key] = new_dist
                    pred[neighbour_key] = node_key

        return SingleNodeShortestPathsCalculationResult(start_node, dist, pred)

    def __get_nodes_enumeration(self):
        return {key: number for key, number in enumerate(self.nodes.keys())}


class PriorityQueue:
    def __init__(self):
        self.q = []

    def add_with_priority(self, item, priority):
        insort_left(self.q, (priority, item), key=lambda element: element[0])

    def pop_min(self):
        pair = self.q.pop(0)
        return pair[1]

    def get_min(self):
        return self.q[0][1]

    def change_priority(self, item, new_priority):
        for i in range(len(self.q)):
            if self.q[i][1] == item:
                break
        else:
            raise ValueError(f'No item {item} in priority queue')
        item = (self.q.pop(i))[1]
        self.add_with_priority(priority=new_priority, item=item)

    def is_empty(self):
        return len(self.q) == 0

    def items_count(self):
        return len(self.q)


class SingleNodeShortestPathsCalculationResult:
    def __init__(self, origin_node_key, dist, pred):  # NOQA
        self.origin_node_key = origin_node_key
        self.__pred = pred  # NOQA
        self.__dist = dist

    def get_distance(self, to_node):
        return self.__dist[to_node]

    def get_path(self, to_node):
        if self.__pred[to_node] is None:
            return None
        path = [to_node]
        active_node = to_node
        while active_node != self.origin_node_key:
            active_node = self.__pred[active_node]
            path.append(active_node)
        return reversed(path)


class InvalidNodeKey(Exception):
    def __init__(self, key):
        super().__init__(f'No "{key}" node found.')
