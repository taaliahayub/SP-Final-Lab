import part1
import part2
import math
import csv
import timeit

connections = {}
stations = {}
g = part1.DirectedWeightedGraph()

# this file is to experiment only on combinations of stations in the same line
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lon1, lat1, lon2, lat2])
    diflon, diflat = lon2 - lon1, lat2 - lat1
    return (2 * math.asin(math.sqrt(math.sin(diflat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diflon / 2) ** 2))) * 6371


def per_line(line_no):
    st = []
    with open("./london_connections.csv", 'r') as london_connections:
        csvreader = csv.reader(london_connections)
        next(csvreader)
        for row in csvreader:
            if int(row[2]) == line_no:
                if int(row[0]) not in st:
                    st.append(int(row[0]))
                if int(row[1]) not in st:
                    st.append(int(row[1]))
    
    with open("./london_stations.csv", 'r') as london_stations:
        csvreader = csv.reader(london_stations)
        next(csvreader)
        for row in csvreader:
            if int(row[0]) in st:
                stations[int(row[0])] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]

    return st

def make_connections(line_no):
    with open("./london_connections.csv", 'r') as london_connections:
        csvreader = csv.reader(london_connections)
        next(csvreader)
        for row in csvreader:
            if int(row[2]) == line_no:
                if int(row[0]) not in g.adj:
                    g.add_node(int(row[0]))
                    connections[int(row[0])] = []
                if int(row[1]) not in g.adj:
                    g.add_node(int(row[1]))
                    connections[int(row[1])] = []
                g.add_edge(int(row[0]), int(row[1]), haversine(float(stations[int(row[0])][0]), float(stations[int(row[0])][1]), float(stations[int(row[1])][0]), float(stations[int(row[0])][1])))
                g.add_edge(int(row[1]), int(row[0]), haversine(float(stations[int(row[0])][0]), float(stations[int(row[0])][1]), float(stations[int(row[1])][0]), float(stations[int(row[0])][1])))
                connections[int(row[0])].append([int(row[1]), row[2], row[3]])
                connections[int(row[1])].append([int(row[0]), row[2], row[3]])


def populate_heuristic(destination):
    heuristic = {}
    for i in stations:
        heuristic[i] = haversine(float(stations[i][0]), float(stations[i][1]), float(stations[destination][0]), float(stations[destination][1]))
    return heuristic

lines = [1, 3, 4, 9]
one_line = []
for i in lines:
    one_line += per_line(i)
    make_connections(i)

pairs = []
for i in range(len(one_line)):
    for j in range(i, len(one_line)):
        if i != j:
            pairs.append((one_line[i], one_line[j]))

time_astar = []
time_dijkstra = []
time_diff = []
a_star_w = 0
djikstra_w = 0
runs = 0

for i in pairs:
    runs += 1
    source = i[0]
    destination = i[1]
    heuristic = populate_heuristic(i[1])
    temp_astar = 0
    temp_dijkstra = 0
    for j in range(0, 10):
        # A*
        start = timeit.default_timer()
        part2.a_star(g, source, destination, heuristic)
        end = timeit.default_timer()
        total = end - start
        temp_astar += total
        #dijkstra
        start = timeit.default_timer()
        part1.dijkstra(g, source)
        end = timeit.default_timer()
        total = end - start
        temp_dijkstra += total
    if (temp_astar / 10) < (temp_dijkstra / 10):
        a_star_w += 1
    elif (temp_astar / 10) > (temp_dijkstra / 10): 
        djikstra_w += 1

    time_astar.append(temp_astar / 10)
    time_dijkstra.append(temp_dijkstra / 10)
    print("Pair: " + str(i))
    print("A*: " + str(temp_astar))
    print("Dijkstra: " + str(temp_dijkstra))
    print("Difference in Runtime: " + str(abs(temp_astar - temp_dijkstra)))
    time_diff.append(abs(temp_astar - temp_dijkstra))

aw = (a_star_w / runs) * 100
dw = (djikstra_w / runs) * 100
print("A* wins " + str(aw) + "% of the time")
print("Djikstra wins " + str(dw) + "% of the time")

print("Largest Time Diff: "+ str(max(time_diff)))
print("Smallest Time Diff: " + str(min(time_diff)))
print("Avg Time Diff: " + str((sum(time_diff)) / (len(time_diff))))
