# Traveling Sales Man Problem Solvers

Problem instances in TSPLIB can be found here: http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/
3 Problem instances, burma14.tsp, rl1889.tsp, and rl11849 are included for example.

This program takes the .tsp file (exactly as it is downloaded from the above site) as the input, and create a single output file, named solution.csv. It should contain a single column of city indices, in the order of your solution to the TSP. Also, the program print out the total distance travelled on the standard output. 

# 3 different solvers for TSP 

## 1. brute_tsp_solver.py
Solves the problem brutally, checking every solution available recursively. 

```sh
# in directory "Traveling_Sales_Man_Solver/"
$ python brute_tsp_solver.py burma14.tsp
19.5025891828
$ cat solution.csv
4
3
2
1
9
8
7
6
5
```

## 2. greedy_tsp_solver.py 
Uses greedy algorithm to solve the problem. This algorithm works in the following steps.

1. Choose a random node to begin with and mark it visited.
2. Move to the neighboring node that is closest to the last node and mark it visited.
3. Repeat step 2 until all the nodes are visited.
4. repeat step 1~3 with different random node to begin with, 10 times each. Each repetition will produce one path as solution.
5. out of the 10 solutions, choose the path with minimum distance and return it.

1 Global Variable : num_of_path (number of paths to produce as answers)

```sh
# in directory "Traveling_Sales_Man_Solver/"
$ python greedy_tsp_solver.py burma14.tsp
20.9311605987
$ cat solution.csv
1
8
9
2
3
4
6
7
5
```

## 3. greedy_merge_tsp_solver.py
Chooses 10 random nodes to begin with. With every iteration, each of the 10 paths spread out using greedy algorithm. If the closest node from one path is end point of another path, 2 paths are merged while iterating. After all iterations, the paths that are not yet connected are merged. Final path is returned as solution. Detailed algorithm is explained below.

1. Choose 10 random nodes to begin with which will spread into 10 different paths.
2. For every path, spread out the path to the neighboring node that is closest to the either of the end nodes of the path (There are 2 end nodes for each path). If the closest node from one path is end point of another path, 2 paths are merged. 
3. Repeat step 2 until all the nodes are visited.
4. Merge the paths that are not yet connected into 1 path and return it as solution.

1 Global Variable: number_of_paths (number of paths to produce to merge)

```sh
# in directory "Traveling_Sales_Man_Solver/"
$ python greedy_merge_tsp_solver.py burma14.tsp
19.8527665421
$ cat solution.csv
5
7
6
4
3
2
8
1
9
```

# Common problems and solutions
 1. When the Global Variable, number_of_paths or num_of_path is set too large, program can get trapped in an infinite loop.

 2. Currently, solvers only support the problem format that are exactly the same the the problems instances that are included(burma14.tsp, rl1889.tsp, and rl11849). For new problem instances, must change the format of the problem to match the format of the example problem instances. Currently all solvers, skips 3 lines, read the dimension, skips 2 more lines, than read the node coordination.