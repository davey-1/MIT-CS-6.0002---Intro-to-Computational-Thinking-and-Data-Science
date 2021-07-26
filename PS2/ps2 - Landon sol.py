# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:02:29 2021

@author: lando 
"""

# 6.0002 Problem Set 2
# Graph optimization
# Name: David Sheu
# Time: 5/8/2021

# Objective: Find the shortest path from one MIT building to another

import unittest
from copy import deepcopy
from graph import Digraph, Node, WeightedEdge

# Problem 2: Build up the Campus Map
# Problem 2a: Design your graph
#
# The graph's nodes represent buildings on MIT campus.
# The graph's edges represent one-way traversable paths between buildings.

# Problem 2b: Implement load_map

def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    print("Loading map from file...")

    gr = Digraph()

    file = open(map_filename)

    
    for line in file:
        
        ll = line.split(' ')
        # The components of `ll` are already strings
        n0 = Node(str(ll[0]))
        n1 = Node(str(ll[1]))

        if not gr.has_node(n0):
            gr.add_node(n0)

        if not gr.has_node(n1):
            gr.add_node(n1)

        e = WeightedEdge(n0,n1,int(ll[2]),int(ll[3].rstrip()))
                    
        gr.add_edge(e)
                    
        # note: for WeightedEdge, have to add src and dest as nodes,
        #       not just values corresponding to those nodes

    return gr


# Problem 2c: Test load_map
# Include the lines used to test load_map below, but comment them out
#
#load_map("mit_map.txt")


# Problem 3: Find the Shortest Path using Optimized Search Method
# Problem 3a: Objective function
# What is the objective function for this problem? What are the constraints?
#
# Answer: The objective function for this problem is to find the shortest path
#       between two buildings using optimized depth first search.
#       The constraint is to not exceed a maximum distance traveled
#       outdoors on the path we determine is shortest.

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number/string at which to start
        end: string
            Building number/string at which to end
        path: list composed of [List[str], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance which can be spent outdoors on a path
            (our constraint)
        best_dist: int 
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # Start a new iteration
    # Add the new starting position to the end of the path
    path[0] = path[0] + [start]
    
    # Print the path
    print('path=',path)
    
    # If either node we are searching for is not in the graph, raise an error
    if not (digraph.has_node(Node(start)) and digraph.has_node(Node(end))):
        raise ValueError("Start or end node not found in digraph.")
        
    # If the new starting point is the target destination, return the current path
    if start == end:
        print('start==end, path =',path[0])
        return path[0]
    
    # Otherwise,
    else:
        # Loop through the nodes that the starting node leads to
        for W_E in digraph.get_edges_for_node(Node(start)):
                
            child = W_E.get_destination()
                 
            # Print each node as it searches
            print('start=',start,'child=',child,', end=',end)

            # If the node it is searching is not already part of the path,
            if str(child) not in path[0]: 
                # For optimization, refuse to search down any path where
                # the total distance is greater than the current best path
                # or the outdoor distance is greater than the constraint
                test_dist, test_outdoor = get_distance(digraph, path[0] + [str(child)])
                if test_dist > best_dist or test_outdoor > max_dist_outdoors:
                    continue
                
                # Recurse; search starting from each destination node
                # Store the path it returns as the new path to check
                #                       graph,   new node, target, the path til now,
                #                               constraint, best distance, best path
                newPath = get_best_path(digraph, str(child), end, deepcopy(path), 
                                                max_dist_outdoors, best_dist, best_path)
                
                # Get the total and outdoor distances for the new path
                path[1], path[2] = get_distance(digraph, newPath)
                
                # If the total distance is less that the best_distance so far,
                # and the outdoor distance fits the constraint
                if path[1] < best_dist and path[2] <= max_dist_outdoors and bool(newPath):
                    # Store the new best distance and best path; best path
                    # starts out as an empty list and best distance is an
                    # arbitrarily large number
                    best_dist = path[1]
                    best_path = newPath
                    
                    # Print the new best distance and path
                    print("Update: best_dist:",best_dist,", best_path:",best_path)
    
    return best_path

def get_distance(digraph, path):
    
    t_d = 0
    t_o_d = 0
    
    # print("get_distance called on:",path)
    
    ### Traverse the path and update path distances
    for i in range(len(path)-1):
    
        ### For each WeightedEdge that matches the node of path[i]
        for W_E in digraph.get_edges_for_node(Node(path[i])):
            
            ###if that WeightedEdge's destination equals the next node in path...
            if W_E.dest == Node(path[i+1]):
                
                ###add WeightedEdge's total_dist and total_outdoor_dist to the path totals
                t_d = t_d + W_E.total_distance
                t_o_d = t_o_d + W_E.outdoor_distance  
                
    return t_d, t_o_d
                

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    
    ### Note: Unlike get_best_path, directed_dfs also has a max_total_dist as a constraing  
    
    ###test code to see if get_best_path returns anything... which it doesn't yet
    ###test code does not include the constraint of max_total_distance yet
        
    
    best_path = get_best_path(digraph, start, end,
                              [[],max_total_dist,max_dist_outdoors],
                              max_dist_outdoors, max_total_dist, [])
      
    print("DFS best_path =",best_path)

    (bp_td, bp_tod) = get_distance(digraph, best_path)
                    
    if best_path != [] and bp_td < max_total_dist:
        return best_path

    else:
        raise ValueError("no path that meets the criteria exists")
    



# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")
        
    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)
    
    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))
    
    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)
    
    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
    
    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])
    
    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)
    
    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])
    
    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)
    
    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])
    
    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)
    
    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)
    
    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)
    

if __name__ == "__main__":
    unittest.main()