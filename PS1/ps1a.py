###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

file_name = "ps1_cow_data.txt"


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(filename)
    # wordlist: list of strings
    cow_dir= {}
    for line in inFile:
        templist = line.split(',')
        cow_dir[templist[0]] = int(templist[1])
    print("  ", len(cow_dir), "cows loaded.")
    return cow_dir
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #pseudocode
    
    #sort dictionary?
    
    #greedy function
    
    cowsCopy = sorted(cows.items(), key = lambda x:x[1], reverse = True)
    #cows.items() splits dictionary into list of tuples.
        
    alltrips = []
    tripX = []
    trip_load = limit
        
    for i in range(len(cowsCopy)):
        cow = cowsCopy[i]
                        
        if cow[1] > limit:
            #cow's too heavy? forget it
            pass

        elif (trip_load - cow[1]) < 0:

            #send previous load and reset counter
            if len(tripX) > 0:
                alltrips.append(tripX)                
                tripX = []
                trip_load = limit
            
            #add cow to new load
            tripX.append(cow[0])
            trip_load = trip_load - cow[1]
                   
        else:
            #add cow to new load
            tripX.append(cow[0])
            trip_load = trip_load - cow[1]
     
    #send last load if one exists
    if len(tripX) > 0:
        alltrips.append(tripX)
            
        
    return alltrips

            



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    
    partdict = {}
    
    lowest = limit
    #scorekeeper for list with the fewest trips
    
    
    
    for partition in get_partitions(cows):
        
        #partition is a list of partitions
        
        for trip in partition:
            tripweight = 0
            for cow in trip:
                if cow == 'void':
                    pass
                
                else: 
                    tripweight = tripweight + cows[cow]
            #gets the weight of a given trip in a partition
            
                if tripweight > limit:
                    partition.append(['void'])
                    break
            #marks a partition as void if one of the trips exceeds weight
            
        
        #after each iteration of this loop, partition should either be void or not void
        
        void = ['void']
        
        if void not in partition:
            numtrips = len(partition)
            #intermediate step to get the number of trips for each partition

            partdict[numtrips] = partition
            #if not void, add it to the partition list
            
            if numtrips < lowest:
                lowest = numtrips
                lowlist = partdict[numtrips]
                #set lowlist if numtrips is the lowest we've seen
        
    #result is a dictionary of partitions. key = number of trips.  No duplicate keys!
    
    
        
    return lowlist


        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here

    #brute length & time
    startbrute = time.time()
    
    brute = brute_force_cow_transport(load_cows(file_name))
    
    endbrute = time.time()
    brutetime = endbrute - startbrute
    
    #greedy length & time
    startgreedy = time.time()
    
    greedy = greedy_cow_transport(load_cows(file_name))
        
    endgreedy = time.time()
    greedytime = endgreedy - startgreedy
    

    print('Brute trips:',len(brute))
    print('Brute timing:', brutetime)
    
    print('Greedy trips:', len(greedy))
    print('Greedy timing:', greedytime)
    
    
    
    
compare_cow_transport_algorithms()



