import sys
import math

sys.setrecursionlimit(20000)

nodes_to_visit = [] #list that stores nodes that are unvisited visit.
paths = []          #list that stores paths.
number_of_paths = 10

class path:
    def __init__(self, origin_node):
        self.end_a = origin_node
        self.end_b = origin_node
        self.visit_order = [origin_node]

def minconn_search(num_of_paths):
    path_size = len(nodes_to_visit)/num_of_paths    
    
    for i in range(0,num_of_paths):
        if i*path_size >= len(nodes_to_visit):
            break

        # print "appending node " + str(i*path_size) + " to the paths"
        origin_node = nodes_to_visit[i*path_size]
        nodes_to_visit.remove(origin_node)
        paths.append(path(origin_node))
    
    answer = spread()
    return answer

def spread():

    # spread out each paths one by one with the closest node.
    # If the closest node is in nodes_to_visit list, just add the node.
    # Else if, the closest node is end node of another graph, merge the two graphs
    # Since there are two end nodes for each path, it is neccessary to check both nodes.
    while(len(nodes_to_visit) != 0):
        for path in paths:
            if len(nodes_to_visit) == 0:
                break

            # find the closest node in node_to_visit from each of the 2 end points
            closest_node_a = closest_node(path.end_a, nodes_to_visit)
            node_a_dist = dist(closest_node_a,path.end_a)
            closest_node_b = closest_node(path.end_a, nodes_to_visit)
            node_b_dist = dist(closest_node_b, path.end_b)

            # find the closest node within the end points of path in paths_to_compare, 
            # which is list of path without the path that is being compared,
            # from each of the 2 end points 
            closest_path_a = None
            closest_path_b = None
            flag_from_a_to_a = True
            flag_from_b_to_a = True
            path_a_dist = -1
            path_b_dist = -1
            if(len(paths) > 1):
                paths_to_compare = list(paths)
                paths_to_compare.remove(path)
                closest_path_a = paths_to_compare[0]
                closest_path_b = paths_to_compare[0]
                flag_from_a_to_a = True
                flag_from_b_to_a = True
                path_a_dist = dist(path.end_a, closest_path_a.end_a)
                path_b_dist = dist(path.end_b, closest_path_a.end_a)

                for path_ in paths_to_compare:
                    if dist(path.end_a, path_.end_a) < path_a_dist:
                        closest_path_a = path_
                        path_a_dist = dist(path.end_a, path_.end_a)
                        flag_from_a_to_a = True
                    if dist(path.end_a, path_.end_b) < path_a_dist:
                        closest_path_a = path_
                        path_a_dist = dist(path.end_a, path_.end_b)
                        flag_from_a_to_a = False
                    if dist(path.end_b, path_.end_a) < path_b_dist:
                        closest_path_b = path_
                        path_b_dist = dist(path.end_b, path_.end_a)
                        flag_from_b_to_a = True
                    if dist(path.end_b, path_.end_b) < path_b_dist:
                        closest_path_b = path_
                        path_b_dist = dist(path.end_b, path_.end_b)
                        flag_from_b_to_a = False

            # among the 4 nodes that are closest, choose the one with 
            # minimum distance, and take appropriate action
            distances = [node_a_dist, node_b_dist, path_a_dist, path_b_dist]
            if (node_a_dist == min([n for n in distances if n>0])):
                nodes_to_visit.remove(closest_node_a)
                path.visit_order.insert(0,closest_node_a)
                path.end_a = closest_node_a
            elif (node_b_dist == min([n for n in distances if n>0])):
                nodes_to_visit.remove(closest_node_b)
                path.visit_order.append(closest_node_b)
                path.end_b = closest_node_b
            elif (path_a_dist == min([n for n in distances if n>0])):
                # print "merge a!"
                paths.remove(closest_path_a)
                merge_path(path,closest_path_a,flag_from_a_to_a,flag_from_b_to_a)
            elif (path_b_dist == min([n for n in distances if n>0])):
                # print "merge b!"
                paths.remove(closest_path_b)
                merge_path(path,closest_path_b,flag_from_a_to_a,flag_from_b_to_a)

    # merge all the paths that are not yet merged in to the merged_path
    merged_path = paths.pop(0)
    for i in range(0, len(paths)):
        min_dist_path = paths[0]
        min_dist = dist(merged_path.end_a, min_dist_path.end_a)
        flag_from_a = True
        flag_to_a = True
        for path_to_merge in paths:
            if (dist(merged_path.end_a, path_to_merge.end_a) < min_dist):
                min_dist_path = path_to_merge
                min_dist = dist(merged_path.end_a, path_to_merge.end_a)
                flag_from_a = True
                flag_to_a = True
            if (dist(merged_path.end_a, path_to_merge.end_b) < min_dist):
                min_dist_path = path_to_merge
                min_dist = dist(merged_path.end_a, path_to_merge.end_b)
                flag_from_a = True
                flag_to_a = False
            if (dist(merged_path.end_b, path_to_merge.end_a) < min_dist):
                min_dist_path = path_to_merge
                min_dist = dist(merged_path.end_b, path_to_merge.end_a)
                flag_from_a = False
                flag_to_a = True
            if (dist(merged_path.end_b, path_to_merge.end_b) < min_dist):
                min_dist_path = path_to_merge
                min_dist = dist(merged_path.end_b, path_to_merge.end_b)
                flag_from_a = False
                flag_to_a = False

        paths.remove(min_dist_path) 
        merge_path(merged_path, min_dist_path, flag_from_a, flag_to_a)
        # print "merge final"

    return merged_path.visit_order


#calculate distance between two nodes
def dist(node_x, node_y):
    return math.sqrt((node_x[1]-node_y[1])**2 + (node_x[2]-node_y[2])**2)

# find the closest node in the list nodes from the node
def closest_node(node, nodes):
    #find the node that is closest distance from the last node.
    closest_node = nodes[0]
    for end_node in nodes:
        if dist(node, end_node) < dist(node, closest_node):
            closest_node = end_node
    return closest_node

# merge path_a and path_b into path_a,
# with auxiliary information of flag_from_a and flag_from_b
def merge_path(path_a, path_b, flag_from_a, flag_to_a):
    if flag_from_a == True and flag_to_a == True:
        path_a.end_a = path_b.end_b
        path_b.visit_order.reverse()
        path_a.visit_order = path_b.visit_order + path_a.visit_order
    if flag_from_a == True and flag_to_a == False:
        path_a.end_a = path_b.end_a
        path_a.visit_order = path_b.visit_order + path_a.visit_order
    if flag_from_a == False and flag_to_a == True:
        path_a.end_b = path_b.end_b
        path_a.visit_order = path_a.visit_order + path_b.visit_order
    if flag_from_a == False and flag_to_a == False:
        path_a.end_b = path_b.end_a
        path_b.visit_order.reverse()
        path_a.visit_order = path_a.visit_order + path_b.visit_order


#open tsp file that is passed as argument as read only
f = open(sys.argv[1],'r')

#ignore first 3 lines  
for x in xrange(1,4):
    f.readline()

#read dimension of tsp
dimension = int(f.readline().split()[2])
# print "dimension: " + str(dimension)

#ignore next 2 lines  
for x in xrange(1,3):
    f.readline()

#read NODE_COORD_SECTION and store it in nodes_to_visit
for x in xrange(0,dimension):
    nodes_to_visit.append(
        map(float,(f.readline().split())))

nodes_to_visit_copy = list(nodes_to_visit)

answer = minconn_search(number_of_paths)

#calculate minimum distance
mindistance_answer = 0
for i in range(1,len(answer)):
    mindistance_answer = mindistance_answer + dist(answer[i-1],answer[i])
print mindistance_answer

f_solution = open("solution.csv", 'w')
for node in answer:
    f_solution.write(str(int(node[0])) + "\n")
f_solution.close()

#close file
f.close()


