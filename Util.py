import random
import math

def levelNumber(leaf):          # returns the level the leaf is on (used in getMaxLevel)
    level = 0
    while leaf > 1:
        level+=1
        leaf = leaf >> 1
		
    return level

def revBin(num):       # num is an integer (not in binary), returns reversed binary number
    return int(bin(num)[::-1][:-2],2)
    
def getMaxLevel(leaf1, leaf2):
    if levelNumber(leaf1) > levelNumber(leaf2):
        leaf1 = leaf1 >> 1
    elif levelNumber(leaf1) < levelNumber(leaf2):
        leaf2 = leaf2 >> 1

    # now leaf1 and leaf2 are on the same level

    revBin(leaf1)
    revBin(leaf2)
    diff = leaf1 ^ leaf2	      # bitwise difference
    t = (diff & (-diff)) << 1 - 1
    t2 = revBin(t)
    t3 = revBin(t2 & (-t2))
    
    return int(math.log(t3, 2))
    
    """xdiff = 0

    while diff > 0:
        b = b >> 1
        xdiff+=1
    
    maxLevel = levelNumber(leaf1) - diff
	
    return maxLevel"""

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
