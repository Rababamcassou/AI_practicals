import heapq
from prettytable import PrettyTable


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []  # Liste der Kanten
        self.parent = None  # Referenz auf den Elternknoten
        self.cost = 0  # Kosten für UCS

    def __lt__(self, other):
        return self.cost < other.cost


class Edge:
    def __init__(self, edge):
        self.start = edge[0]
        self.end = edge[1]
        self.value = edge[2]


class Queue:
    def __init__(self, mode='FIFO'):
        self.mode = mode
        self.items = []
        self.priority_items = []

    def is_empty(self):
        if self.mode == 'PRIO':
            return len(self.priority_items) == 0
        return len(self.items) == 0

    def enqueue(self, item, priority=None):
        if self.mode in ['FIFO', 'LIFO']:
            self.items.append(item)
        elif self.mode == 'PRIO':
            heapq.heappush(self.priority_items, (priority, item))

    def dequeue(self):
        if self.mode == 'FIFO':
            if not self.is_empty():
                return self.items.pop(0)
            else:
                raise IndexError("Dequeue from an empty queue")
        elif self.mode == 'LIFO':
            if not self.is_empty():
                return self.items.pop()
            else:
                raise IndexError("Dequeue from an empty queue")
        elif self.mode == 'PRIO':
            if not self.is_empty():
                return heapq.heappop(self.priority_items)[1]
            else:
                raise IndexError("Dequeue from an empty queue")

    def size(self):
        if self.mode == 'PRIO':
            return len(self.priority_items)
        return len(self.items)

    def peek(self):
        if self.mode == 'FIFO':
            if not self.is_empty():
                return self.items[0]
            else:
                raise IndexError("Peek from an empty queue")
        elif self.mode == 'LIFO':
            if not self.is_empty():
                return self.items[-1]
            else:
                raise IndexError("Peek from an empty queue")
        elif self.mode == 'PRIO':
            if not self.is_empty():
                return self.priority_items[0][1]
            else:
                raise IndexError("Peek from an empty queue")


class Graph:
    def __init__(self, node_list, edges):
        self.nodes = [Node(name) for name in node_list]
        for e in edges:
            start_node = self.get_node(e[0])
            end_node = self.get_node(e[1])
            if start_node != -1 and end_node != -1:
                start_node.edges.append(Edge((start_node, end_node, e[2])))
                end_node.edges.append(Edge((end_node, start_node, e[2])))

    def get_node(self, name):
        return next((node for node in self.nodes if node.name == name), -1)

    def bfs(self, start, goal):
        start_node = self.get_node(start)
        goal_node = self.get_node(goal)

        if start_node == -1 or goal_node == -1:
            return None

        queue = Queue(mode='FIFO')
        visited = set()
        queue.enqueue(Node(start_node.name))

        while not queue.is_empty():
            current_node = queue.dequeue()
            if current_node.name == goal_node.name:
                return self.reconstruct_path(current_node)

            visited.add(current_node.name)

            for edge in self.get_node(current_node.name).edges:
                if edge.end.name not in visited:
                    child_node = Node(edge.end.name)
                    child_node.parent = current_node  # Set parent for path reconstruction
                    queue.enqueue(child_node)

        return None

    def dfs(self, start, goal):
        start_node = self.get_node(start)
        goal_node = self.get_node(goal)

        if start_node == -1 or goal_node == -1:
            return None

        stack = Queue(mode='LIFO')
        visited = set()
        stack.enqueue(Node(start_node.name))

        while not stack.is_empty():
            current_node = stack.dequeue()
            if current_node.name == goal_node.name:
                return self.reconstruct_path(current_node)

            if current_node.name not in visited:
                visited.add(current_node.name)

                for edge in self.get_node(current_node.name).edges:
                    if edge.end.name not in visited:
                        child_node = Node(edge.end.name)
                        child_node.parent = current_node  # Set parent for path reconstruction
                        stack.enqueue(child_node)

        return None

    def ucs(self, start, goal):
        start_node = self.get_node(start)
        goal_node = self.get_node(goal)

        if start_node == -1 or goal_node == -1:
            return None

        priority_queue = Queue(mode='PRIO')
        visited = set()
        priority_queue.enqueue(Node(start_node.name), 0)

        while not priority_queue.is_empty():
            current_node = priority_queue.dequeue()

            if current_node.name == goal_node.name:
                return self.reconstruct_path(current_node)

            if current_node.name in visited:
                continue

            visited.add(current_node.name)

            for edge in self.get_node(current_node.name).edges:
                if edge.end.name not in visited:
                    new_cost = current_node.cost + edge.value
                    child_node = Node(edge.end.name)
                    child_node.parent = current_node  # Track parent for path reconstruction
                    child_node.cost = new_cost  # Set the cost for UCS
                    priority_queue.enqueue(child_node, new_cost)

        return None

    def reconstruct_path(self, node):
        path = []
        total_cost = 0
        while node is not None:
            path.append(node.name)
            # If the node has a parent, add the cost of the edge to the total cost
            if node.parent is not None:
                for edge in self.get_node(node.name).edges:
                    if edge.end.name == node.parent.name:
                        total_cost += edge.value
                        break
            node = node.parent
        return path[::-1], total_cost  # Return reversed path and total cost

    def print_graph(self):
        node_list = self.nodes
        t = PrettyTable([' '] + [node.name for node in node_list])
        for node in node_list:
            edge_values = ['X'] * len(node_list)
            for edge in node.edges:
                edge_values[next((i for i, e in enumerate(node_list) if e.name == edge.end.name), -1)] = edge.value
            t.add_row([node.name] + edge_values)
        print(t)


if __name__ == "__main__":
    romania = Graph(
        ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa', 'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi', 'Me', 'Bu', 'Dr', 'Ef',
         'Cr', 'Gi'],
        [('Or', 'Ze', 71), ('Or', 'Si', 151), ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
         ('Ia', 'Va', 92), ('Ar', 'Si', 140), ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
         ('Si', 'Ri', 80), ('Fa', 'Bu', 211), ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
         ('Ri', 'Cr', 146), ('Ti', 'Lu', 111), ('Lu', 'Me', 70), ('Me', 'Dr', 75),
         ('Dr', 'Cr', 120), ('Cr', 'Pi', 138), ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
         ('Bu', 'Ur', 85), ('Ur', 'Hi', 98), ('Hi', 'Ef', 86)]
    )

    start = 'Bu'
    goal = 'Ti'

    # BFS
    bfs_path, bfs_cost = romania.bfs(start, goal)
    print("BFS Path from {} to {}: {} with cost: {}".format(start, goal, bfs_path, bfs_cost))

    # DFS
    dfs_path, dfs_cost = romania.dfs(start, goal)
    print("DFS Path from {} to {}: {} with cost: {}".format(start, goal, dfs_path, dfs_cost))

    # UCS
    ucs_path, ucs_cost = romania.ucs(start, goal)
    print("UCS Path from {} to {}: {} with cost: {}".format(start, goal, ucs_path, ucs_cost))