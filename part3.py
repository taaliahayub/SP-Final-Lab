import part1
import part2
import math
import csv
import timeit

connections = {}
stations = {}
g = part1.DirectedWeightedGraph()

# returns the as-the-crow-flies distance between 2 points
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lon1, lat1, lon2, lat2])
    diflon, diflat = lon2 - lon1, lat2 - lat1
    return (2 * math.asin(math.sqrt(math.sin(diflat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diflon / 2) ** 2))) * 6371

# gathers tube stations in a dictionary
with open("./london_stations.csv", 'r') as london_stations:
    csvreader = csv.reader(london_stations)
    next(csvreader)
    for row in csvreader:
        stations[int(row[0])] = [row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
        

# adds edges using directed graph (both directions), also stores in connections dictionary
with open("./london_connections.csv", 'r') as london_connections:
    csvreader = csv.reader(london_connections)
    next(csvreader)
    for row in csvreader:
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

# get all the distances from all the stations to the destination station
def populate_heuristic(destination):
    heuristic = {}
    for i in stations:
        heuristic[i] = haversine(float(stations[i][0]), float(stations[i][1]), float(stations[destination][0]), float(stations[destination][1]))
    return heuristic

# get pairs one way (1,1), (1,2) ... tingyu confirmed 
def combination_stations():
    local_stations = []
    pairs = []
    for i in stations.keys():
        local_stations.append(int(i))
    local_stations.sort()

    for i in range(len(local_stations)):
        for j in range(int(i), len(local_stations)):
            pairs.append((local_stations[i], local_stations[j]))
    return pairs

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
    return st

# ==============================================================================================================
# gets the time it takes for each algorithm to run each experiment 
print("================================================================================")
print("")
pairs = combination_stations()
time_astar = []
time_dijkstra = []
dijkstra_wins = []
a_star_w = 0
djikstra_w = 0
runs = 0
check = pairs[9000:]
for i in check:
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
    else: 
        djikstra_w += 1
        dijkstra_wins.append(i)
    time_astar.append(temp_astar / 10)
    time_dijkstra.append(temp_dijkstra / 10)
    print("Pair: " + str(i))
    print("A*: " + str(temp_astar))
    print("Dijkstra: " + str(temp_dijkstra))
    print("Difference in Runtime: " + str(abs(temp_astar - temp_dijkstra)))

aw = (a_star_w / runs) * 100
dw = (djikstra_w / runs) * 100
print("A* wins " + str(aw) + "% of the time")
print("Djikstra wins " + str(dw) + "% of the time")

# gets the pairs with the largest difference in time and the pairs with the smallest difference
# "(1,3), dijkstra_time, astar_time, dif"
dijkstra_loses = [[(0, 0), 0, 0, 0]]
astar_loses = [[(1, 1), 0, 0, 0]] # must be initialized to (1,1) to prevent key errors, algo very good
smallest_pair = [[(0, 0), 0, 0, 1000000000]]
for i in range(len(check)):
    if (time_dijkstra[i] - time_astar[i] > dijkstra_loses[0][3]):
        dijkstra_loses[0] = [pairs[i], time_dijkstra[i], time_astar[i], time_dijkstra[i] - time_astar[i]]
    if (time_astar[i] - time_dijkstra[i] > astar_loses[0][3]):
        astar_loses[0] = [pairs[i], time_dijkstra[i], time_astar[i], time_astar[i] - time_dijkstra[i]]
    if (abs(time_dijkstra[i] - time_astar[i]) < smallest_pair[0][3] and pairs[i][0] != pairs[i][1]):   
        smallest_pair[0] = [pairs[i], time_dijkstra[i], time_astar[i], abs(time_dijkstra[i] - time_astar[i])]

file = open('dijkstra_wins_v2.txt', 'a')
for pair in dijkstra_wins:
    file.write(str(pair)+'\n')
file.close()

# print(abs(0.00004 - 0.23))
print("")
print("")
print("================================================================================")
print(dijkstra_loses)
print(astar_loses)
print(smallest_pair)
print("================================================================================")
print("")
print("")

# ==================================================================================================
# incorporate line into experiment
print("tube line tests")
print("================================================================================")
lines_used = []
sp = part2.a_star(g, dijkstra_loses[0][0][0], dijkstra_loses[0][0][1], populate_heuristic(dijkstra_loses[0][0][1]))[1]
for i in range(1, len(sp)):
    if i != len(sp) - 1:
        for j in range(len(connections[sp[i]])):
                if connections[sp[i]][j][0] == sp[i + 1]:
                    if connections[sp[i]][j][1] not in lines_used:
                        lines_used.append(connections[sp[i]][j][1])

print("tube lines on dijkstra loses:")
print(sp)
print("number of lines used: " + str(len(lines_used)))
print(lines_used)

print("================================================================================")

lines_used = []
sp = part2.a_star(g, astar_loses[0][0][0], astar_loses[0][0][1], populate_heuristic(astar_loses[0][0][1]))[1]
for i in range(1, len(sp)):
    if i != len(sp) - 1:
        for j in range(len(connections[sp[i]])):
                if connections[sp[i]][j][0] == sp[i + 1]:
                    if connections[sp[i]][j][1] not in lines_used:
                        lines_used.append(connections[sp[i]][j][1])

print("a star tube lines on astar loses:")
print(sp)
print("number of lines used: " + str(len(lines_used)))
print(lines_used)

print("================================================================================")

lines_used = []
sp = part2.a_star(g, smallest_pair[0][0][0], smallest_pair[0][0][1], populate_heuristic(smallest_pair[0][0][1]))[1]
for i in range(1, len(sp)):
    if i != len(sp) - 1:
        for j in range(len(connections[sp[i]])):
                if connections[sp[i]][j][0] == sp[i + 1]:
                    if connections[sp[i]][j][1] not in lines_used:
                        lines_used.append(connections[sp[i]][j][1])

print("tube lines on smallest pair:")
print(sp)
print("number of lines used: " + str(len(lines_used)))
print(lines_used)

print("number of pairs: " + str(len(pairs)))
