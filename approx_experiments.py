import part1 as d
import matplotlib.pyplot as plot

g = d.DirectedWeightedGraph()
num_of_k = []
dist_dyk = []
dist_bell = []
y = 0
def repeatExperiment(beg, end, skip, inner_itereration):
    y = 7
    for x in range(beg, end, skip):
        num_of_k.append(x)
        total_dist_bell = 0
        total_dist_dyk = 0
        y = y + 0.1

        for _ in range(0, inner_itereration):
            graph = d.create_random_complete_graph(50, x)
            total_dist_bell += d.total_dist(d.bellman_ford(graph, 0))
            total_dist_dyk += d.total_dist(d.bellman_ford_approx(graph, 0, y))
        dist_dyk.append(total_dist_dyk / inner_itereration)
        dist_bell.append(total_dist_bell / inner_itereration)
 
repeatExperiment(1, 100, 5, 30)
plot.title("Average Total Distance vs Maximum Edge Weight in Graph")
plot.xlabel("Maximum Weight of Edges")
plot.ylabel("Average Total Distance")
plot.plot(num_of_k, dist_dyk, 'b', label="Average Distance Bellman-Ford Approx")
plot.plot(num_of_k, dist_bell, 'g', label="Average Distance Bellman-Ford")
plot.legend()
plot.show()
