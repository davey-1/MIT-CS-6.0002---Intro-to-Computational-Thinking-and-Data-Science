###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    if len(egg_weights) == 1:
        result = target_weight

    #if heaviest egg > target weight, run function without it.
    elif egg_weights[-1] > target_weight:
        result = dp_make_weight(egg_weights[0:-1], target_weight)
        
    
    else:
        #define what value is for consideration
        toConsider = egg_weights[-1]
        
        #Explore adding the value
        new_target = target_weight - toConsider
        withVal = 1 + dp_make_weight(egg_weights, new_target)
        
        #Explore not adding the value
        #Next value for consideration is at the index before the previous
        withoutVal = dp_make_weight(egg_weights[0:-1], target_weight)    
    

        if withVal < withoutVal:
            result = withVal
        
        else: 
            result = withoutVal
                    
    '''
    This is the greedy algorithm....old code!
    
    #find out how many of the heaviest eggs can fit
    heavyeggcount = 0
    new_target = target_weight
    
    while egg_weights[-1] * (heavyeggcount + 1) <= target_weight:
        heavyeggcount += 1
        new_target -= egg_weights[-1]

    #return the result plus the sum of all other subsets given their sub-weights
    result = heavyeggcount  + dp_make_weight(egg_weights[0:-1], new_target)
    '''
    
    return result
    
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
    
