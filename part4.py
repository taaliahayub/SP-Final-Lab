import min_heap
import random

class Graph:
    def add_node(self, node:int) -> None:
        self.adj[node] = []
        
    def add_edge(self, node1:int, node2:int, weight:float) -> None:
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def number_of_nodes(self) -> int:
        return len(self.adj)

    def adjacent_nodes(self, node:int) -> list[int]:
        return self.adj[node]

    def are_connected(self, node1:int, node2:int) -> bool:
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def w(self, node1:int, node2:int) -> float:
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]
        

class SPAlgorithm:
    def calc_sp(self, graph: Graph, source: int, dest: int) -> float:
        if self.dist == None:
            return self.func(graph, source, dest)
        else:
            self.func(graph, source)
            return self.dist.get(dest)

class ShortPathFinder:
    def __init__(self) -> None:
        self.graph = None
        self.spalgorithm = None
    def calc_short_path(self, source: int, dest: int) -> float:
        return self.spalgorithm.calc_sp(self.graph, source, dest) 
    def set_graph(self, graph: Graph) -> None:
        self.graph = graph
    def set_algorithm(self, algorithm: SPAlgorithm) -> None:
        self.spalgorithm = algorithm

class WeightedGraph(Graph):

    def __init__(self):
        self.adj = {}
        self.weights = {}

class HeuristicGraph(WeightedGraph):
    def __init__(self):
        self.adj = {}
        self.weights = {}
    
    __heuristic = {
    1: 9, # a
    2: 7, # b
    3: 8, # c
    4: 8, # d
    5: 0, #final destination: e
    6: 6, # f
    7: 3, # g
    8: 6, # h
    9: 4, # i
    10: 4, # j
    11: 3, # k
    12: 6, # l
    13: 10 #start s
    }

    def get_heuristic(self) -> dict[int, float]:
        return self.__heuristic

class Dijkstra(SPAlgorithm):

    def __init__(self):
        self.dist = {}

    def func(self, G, source):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        self.dist = {} #Distance dictionary
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys())

        #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            self.dist[node] = float("inf")
        Q.decrease_key(source, 0)

        #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value
            self.dist[current_node] = current_element.key
            for neighbour in G.adj[current_node]:
                if self.dist[current_node] + G.w(current_node, neighbour) < self.dist[neighbour]:
                    Q.decrease_key(neighbour, self.dist[current_node] + G.w(current_node, neighbour))
                    self.dist[neighbour] = self.dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
        return self.dist

class Bellman_Ford(SPAlgorithm):
    def __init__(self):
        self.dist = {}

    def func(self, G, source):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        self.dist = {} #Distance dictionary
        nodes = list(G.adj.keys())

        #Initialize distances
        for node in nodes:
            self.dist[node] = float("inf")
        self.dist[source] = 0

        #Meat of the algorithm
        for _ in range(G.number_of_nodes()):
            for node in nodes:
                for neighbour in G.adj[node]:
                    if self.dist[neighbour] > self.dist[node] + G.w(node, neighbour):
                        self.dist[neighbour] = self.dist[node] + G.w(node, neighbour)
                        pred[neighbour] = node
        return self.dist

class A_Star2():
    def func(G, s, d, h):
        pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
        dist = {} #Distance dictionary
        shortestpath = [] #list containing the shortest path
        temp = []
        Q = min_heap.MinHeap([])
        nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")
        Q.decrease_key(s, h[s]) #decrease to h[s] bc in while loop we don't take into heuristic while comparing distances
    
    #Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value 
            dist[current_node] = current_element.key - h[current_node]

        # if the heap pops the destination, we already got the shortest path!
            if (current_node == d):
                break

            for neighbour in G.adj[current_node]:
                if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour] and neighbour not in temp:
                    Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour])
                    dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                    pred[neighbour] = current_node
                    temp.append(neighbour)
    
    # we loop through the predecessor dictionary to find the shortest path and then reverse it
        node = d
        shortestpath.append(node)
        while node != s:
            node = pred[node]
            shortestpath.append(node)
        shortestpath.reverse()

        return (pred, shortestpath)
    

class A_Star(SPAlgorithm, A_Star2):
    def __init__(self):
        self.dist = None
    def func(self, G, source, dest):
        h1 = HeuristicGraph().get_heuristic()
        tup = A_Star2.func(G, source, dest, h1)
        sp = tup[1]
        weight = 0
        # get weight between each adj node in sp
        for i in range(len(sp) - 1):
            node1 = sp[i]
            node2 = sp[i + 1]
            w = G.w(node1, node2)
            weight += w
        return weight
