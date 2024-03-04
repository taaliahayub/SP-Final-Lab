import min_heap
import part1

heuristic = {
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

def a_star(G, s, d, h):
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

g = part1.DirectedWeightedGraph()
g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_node(4)
g.add_node(5)
g.add_node(6)
g.add_node(7)
g.add_node(8)
g.add_node(9)
g.add_node(10)
g.add_node(11)
g.add_node(12)
g.add_node(13)
g.add_edge(1, 13, 7)
g.add_edge(1, 2, 3)
g.add_edge(1, 4, 4)
g.add_edge(2, 13, 2)
g.add_edge(2, 1, 3)
g.add_edge(2, 4, 4)
g.add_edge(2, 8, 1)
g.add_edge(3, 13, 3)
g.add_edge(3, 12, 2)
g.add_edge(4, 1, 4)
g.add_edge(4, 2, 4)
g.add_edge(4, 6, 5)
g.add_edge(5, 7, 2)
g.add_edge(5, 11, 5)
g.add_edge(6, 4, 5)
g.add_edge(6, 8, 3)
g.add_edge(7, 8, 2)
g.add_edge(7, 5, 2)
g.add_edge(8, 2, 1)
g.add_edge(8, 6, 3)
g.add_edge(8, 7, 2)
g.add_edge(9, 12, 4)
g.add_edge(9, 10, 6)
g.add_edge(9, 11, 4)
g.add_edge(10, 12, 4)
g.add_edge(10, 9, 6)
g.add_edge(10, 11, 4)
g.add_edge(11, 9, 4)
g.add_edge(11, 10, 4)
g.add_edge(11, 5, 5)
g.add_edge(12, 3, 2)
g.add_edge(12, 9, 4)
g.add_edge(12, 10, 4)
g.add_edge(13, 1, 7)
g.add_edge(13, 2, 2)
g.add_edge(13, 3, 3)
