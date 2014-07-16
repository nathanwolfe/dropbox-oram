import Util
import Block
import math

class Stash:

    def __init__(self, z):
        self._oldStash = False
        self._nodes = []
        self._z = z
        
    def getSize(self):
        return len(self._nodes)
    
    def addNode(self, block):
        self._nodes.append(block)

    def deleteNode(self, index):
        del self._nodes[index]

    def getNodes(self):
        return self._nodes

    def setNodes(self, someList):
        self._nodes = someList

    def request(self, segID):
        
        for i in range(len(self._nodes)):
            if self._nodes[i].getSegID() == segID:
                return self._nodes.pop(i)                # request just returns the node if found
                       
        return "not found"

    def evict(self, leaf):            # returns list of the blocks that go in each node on the path as a 2d list, should compare IDs and return if found as well
        numLevels = Util.levelNumber(leaf) + 1
        result = [0] * numLevels
        
        for i in range(numLevels):
            result[i] = [Block.Block(0, 0, b"")] * self._z

        stashIter = 0
        full = math.pow(2, numLevels) - 1    # "full vector" which has numLevel digits, and 1 means bucket has room for more
        pathVec = [0] * numLevels           # holds number of blocks in bucket occupied
        
        while stashIter < len(self._nodes):                                  # put nodes in the list where 0th element is 0th level, etc.
            if self._oldStash == False:
                """if leaf == 1:
                #print()
                #print("root")
                bucketPos = pathVec[0]
                result[0][bucketPos] = self._nodes[stashIter]
                self.deleteNode(stashIter)
                pathVec[0] += 1
                if pathVec[0] == self._z:
                    full -= math.pow(2, 0)

                else:"""
                legalLevels = Util.getMaxLevel(leaf, self._nodes[stashIter].getLeaf())     # gets the number that tells which levels are allowed
                #print(str(leaf) + ", " + str(self._nodes[stashIter].getLeaf()))
                #print("legalLevels: "  + str(legalLevels))
                availBuc = int(full) & legalLevels              # gets number that shows which buckets are available and allowed
                #print("availBuc: " + str(availBuc))
                if availBuc == 0:    # if it's 0, then there are no available ones, we move on
                    print("no available")
                    stashIter += 1
                else:
                    print("available")
                    bucketLevel = int(math.log(availBuc, 2))
                    #print("bucketLevel: " + str(bucketLevel))
                    bucketPos = pathVec[bucketLevel]
                    result[bucketLevel][bucketPos] = self._nodes[stashIter]
                    self.deleteNode(stashIter)
                    pathVec[bucketLevel] += 1
                    if pathVec[bucketLevel] == self._z:
                        full -= math.pow(2, bucketLevel)
                    
            
            else:
                curLevel = Util.getMaxLevel(leaf, self._nodes[stashIter].getLeaf())
                nodeEvicted = False 
                
                while curLevel > -1:
                    #print ("another test")
                    # This part of the code can be optimized
                    # You can maintain an array indicating how many blocks have been evicted to each bucket.
                    # Then you do not need to go into each slot.
                    # Tou immediately know whether or not a block can go to a bucket, and if it can, which slot it should go to.
                

                    for treeNodeIter in range(self._z):
                        #print (treeNodeIter)
                        #print (curLevel)
                        if result[curLevel][treeNodeIter].getSegID() == 0:
                            #print ("entering")
                            result[curLevel][treeNodeIter] = self._nodes[stashIter]       # puts the segID of the block in the first available space in the list
                            #print(node.getSegID())
                            self.deleteNode(stashIter)
                            nodeEvicted = True
                            break

                    if nodeEvicted == False:                       # if a node was not evicted, then we move to the next node
                        #print ("enter")
                        curLevel-=1
                        if (curLevel == -1):
                            stashIter+=1
                    else:
                        break

        return result

    def correctLeaves(self, treeSize):
        for node in self._nodes:
            newLeaf = Util.correctLeaf(node.getLeaf(), treeSize, node.getSegID() % 2)
            if newLeaf != None:
                node.setLeaf(newLeaf)
