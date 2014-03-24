def levelNumber(leaf):          # returns the level the leaf is on (used in getMaxLevel)
    level = 0
    while leaf > 1:
        level+=1
        leaf = int (leaf / 2)
    return level

def getMaxLevel(leaf1, leaf2):
    if levelNumber(leaf1) > levelNumber(leaf2):
        leaf1 = int(leaf1/2)
    elif levelNumber(leaf1) < levelNumber(leaf2):
        leaf2 = int(leaf2/2)

    # now leaf1 and leaf2 are on the same level
    
    z = leaf1 ^ leaf2	      # bitwise difference
    diff = 0

    while z > 0:
        z = int(z / 2)
        diff+=1
        
    maxLevel = levelNumber(leaf1) - diff
    
    return maxLevel

def getPathNodes(leaf):           # returns a list of node numbers that are on the given path
    result = []
    while (leaf > 0):
        result.append(leaf)
        leaf = int(leaf / 2)
    return result
