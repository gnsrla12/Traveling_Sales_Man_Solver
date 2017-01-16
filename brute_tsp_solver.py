import sys
import math

#calculate distance between two nodes
def dist(node_x, node_y):
    return math.sqrt((node_x[1]-node_y[1])**2 + (node_x[2]-node_y[2])**2)


#list that stores all answers.
all_answers = []

# recursive function that searches for all possible routes with their distance
# and put them in the list 'all_answers'.
def all_search(visit_order, nodes_to_visit, distance):

    #termination condition
    if len(nodes_to_visit) == 0:
        all_answers.append((distance,list(visit_order)))
        return
    
    else:
        for i in range(0,len(nodes_to_visit)):
            next_node = nodes_to_visit[i]
            if len(visit_order) != 0:
                temp_dist = dist(visit_order[-1],next_node)
            else:
                temp_dist = 0
            
            nodes_to_visit.remove(next_node)
            visit_order.append(next_node)
            all_search(visit_order, nodes_to_visit, distance + temp_dist)
            visit_order.remove(next_node)
            nodes_to_visit.insert(i,next_node)


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
all_search([],nodes, 0)

#find the minimum distance answer among all the solutions
mindistance_answer = all_answers[0]
for answer in all_answers:
    if answer[0] < mindistance_answer[0]:
        mindistance_answer = answer

print mindistance_answer[0]

f_solution = open("solution.csv", 'w')
for node in mindistance_answer[1]:
    f_solution.write(str(int(node[0])) + "\n")
f_solution.close()

#close file
f.close()


