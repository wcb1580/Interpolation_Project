# ENGSCI233: Lab - Combinatorics

# imports
from functions_comblab import *

# create network object
network = Network()
network.read_network('waka_voyage_network.txt')

# TODO - your code here in Task 3
#Task1: Finding the shortest path between Taiwan and Hokianga
source_name="Taiwan"
destination_name="Hokianga"
distance,path=shortest_path(network, source_name, destination_name) #pass both locations into the shortest_path() function
print(path)
print(distance)

#Task2: Finding the pair of islands that have the greatest travel time
list=[]
destination=[]
for node in network.nodes: #append nodes into a destination list and a loop list.
    list.append(node)
    destination.append(node)
single_node_distance=[]
single=[]
total_distance=[]
maximum=[]
single_node_distance1=[]
for node in list: #loop through the loop list
    destination.remove(node) #remove the indexation location from the destination list.
    for i in range(len(destination)):
        distance,path=shortest_path(network,node.name,destination[i].name) #use shortest_path to determine the shortest distance between every location in destination node and the current indexation.
        single_node_distance.append([distance,node.name,destination[i].name])#append relevant information into a check list.
    for i in range(len(single_node_distance)): #check if the travel time appended in the check list is None
        if single_node_distance[i][0]!=None:
            single.append(single_node_distance[i])
    if len(single)==0:#if a node does not have any distination, reset the other lists
        single_node_distance = []
        destination.append(node)
    else: #if a node has distination, record it into the information into the final list
        maximum=max(single)
        total_distance.append(maximum)
        maximum=[]
        single_node_distance=[]
        single=[]
        destination.append(node)
Maximum_time=max(total_distance)[0]
from_node=max(total_distance)[1]
to_node=max(total_distance)[2]
print(from_node ,"and" ,to_node," are the pair islands that has the greatest travel time with", Maximum_time)









