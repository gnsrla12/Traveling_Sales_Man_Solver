import sys
import math

sys.setrecursionlimit(20000)

# number of paths to produce as answers
num_of_path = 3

#list that stores answers given by min_search function.
min_answers = []

#calculate distance between two nodes
def dist(node_x, node_y):
    return math.sqrt((node_x[1]-node_y[1])**2 + (node_x[2]-node_y[2])**2)

# recursive function that searches for all possible routes with their distance
# and put them in the list 'all_answers'.
def min_search(visit_order, nodes_to_visit, distance):

    #termination condition
    if len(nodes_to_visit) == 0:
        min_answers.append((distance,list(visit_order)))
        return
    
    else:

        # ongoing of path
        if len(visit_order) != 0:
            #find the node that is closest distance from the last node.
            closest_node = nodes_to_visit[0]
            for node in nodes_to_visit:
                if dist(visit_order[-1], node) < dist(visit_order[-1], closest_node):
                    closest_node = node

            #continue recursive search with the closest_node
            next_dist = dist(visit_order[-1], closest_node)
            temp_index = nodes_to_visit.index(closest_node)        
            nodes_to_visit.remove(closest_node)
            visit_order.append(closest_node)
            min_search(visit_order,nodes_to_visit, distance + next_dist)
            visit_order.remove(closest_node)
            nodes_to_visit.insert(temp_index,closest_node)

        #beginning of each path    
        else:
            gap = len(nodes_to_visit)/num_of_path
            index = 0
            next_dist = 0
            while index < len(nodes_to_visit):
                # print index
                next_node = nodes_to_visit[index]
                nodes_to_visit.remove(next_node)
                visit_order.append(next_node)
                min_search(visit_order, nodes_to_visit, distance + next_dist)
                visit_order.remove(next_node)
                nodes_to_visit.insert(index,next_node)
                index = index + gap



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

#read NODE_COORD_SECTION and store it in nodes
nodes = []
for x in xrange(0,dimension):
    nodes.append(
        map(float,(f.readline().split())))

#search for all solutions
min_search([],nodes, 0)

#find the minimum distance answer among the solutions
mindistance_answer = min_answers[0]
for answer in min_answers:
    # print answer[0]
    if answer[0] < mindistance_answer[0]:
        mindistance_answer = answer

# print mindistance_answer[1]
print mindistance_answer[0]

f_solution = open("solution.csv", 'w')
for node in mindistance_answer[1]:
    f_solution.write(str(int(node[0])) + "\n")
f_solution.close()

#close file
f.close()