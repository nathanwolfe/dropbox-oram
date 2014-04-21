import random

def levelNumber(leaf):          # returns the level the leaf is on (used in getMaxLevel)
    level = 0
    while leaf > 1:
        level+=1
        leaf = leaf >> 1
		
    return level

def getMaxLevel(leaf1, leaf2):
    if levelNumber(leaf1) > levelNumber(leaf2):
        leaf1 = leaf1 >> 1
    elif levelNumber(leaf1) < levelNumber(leaf2):
        leaf2 = leaf2 >> 1

    # now leaf1 and leaf2 are on the same level
    
    b = leaf1 ^ leaf2	      # bitwise difference
    diff = 0

    while b > 0:
        b = b >> 1
        diff+=1
    
    maxLevel = levelNumber(leaf1) - diff
	
    return maxLevel

def getPathNodes(leaf):           # returns a list of node numbers that are on the given path
    result = []
    while (leaf > 0):
        result.insert(0, leaf)
        leaf = leaf >> 1
    return result

def correctLeaf(leaf, treeSize, bit):
    assert (leaf != 0), "0 leaf"
    newLeaf = leaf
    while newLeaf < int(treeSize / 2) + 1:
        newLeaf = (newLeaf * 2) + bit
    while newLeaf > treeSize:
        newLeaf = int(newLeaf / 2)
    if newLeaf != leaf:
        return newLeaf
