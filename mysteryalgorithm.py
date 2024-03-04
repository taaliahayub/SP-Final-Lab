import part1 as p1
import matplotlib.pyplot as plot
import timeit

num_of_nodes = []
time = []

for i in range(4, 1000):
    num_of_nodes.append(i)
    total_time = 0
    g = p1.create_random_complete_graph(i, 20)
    start = timeit.default_timer()
    p1.mystery(g)
    end = timeit.default_timer()
    total = end - start
    time.append(total_time)

plot.title("No. of Nodes vs. Runtime")
plot.xlabel("No. of Nodes")
plot.ylabel("Runtime")
plot.loglog(num_of_nodes, time, 'g')
plot.show()
