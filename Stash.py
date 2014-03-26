import Util
import Block

class Stash:

    def __init__(self):
        self._nodes = []
        
    def getSize(self):
        return len(self._nodes)
    
    def addNode(self, block):
        self._nodes.append(block)

    def deleteNode(self, index):
        del self._nodes[index]

    def request(self, segID, oper, writeData):
        
        for i in range(len(self._nodes):
            if self._nodes[i].getSegID() == segID:
                if oper == "write":
                    #set leaf to random number, based on tree size
                    self._nodes[i].setData(writeData)
                    return 0
                elif oper == "read":
                    #set leaf to random number, based on number of leaves on the tree
                    return self._nodes[i].getData()
                       
        # if the code reaches here (i.e. did not find the specific block) then 
        # evict based on leaf of segID (uses PosMap), how to access the PosMap? and then remap as well

    def evict(self, leaf):            # returns list of the blocks that go in each node on the path as a 2d list, should compare IDs and return if found as well
        z, numLevels           # in which file would I find these?
        result = [0] * numLevels
        
        for i in range(numLevels):
            result[i] = [-1] * z
        
        for i in range(len(_nodes)):                                  # put nodes in the list where 0th element is 0th level, etc.
            curLevel = Util.getMaxLevel(leaf, self._nodes[i].getLeaf)
            treeNodeIter = 0
            nodeEvicted = False

            while curLevel > -1:
                for treeNodeIter in range(z):
                    if result[curLevel][treeNodeIter] == -1:
                        result[curLevel][treeNodeIter] = self._nodes[i].getSegID       # puts the segID of the block in the first available space in the list
                        # self.deleteNode(i)     the top module should delete the things in the stash once put into the tree
                        nodeEvicted = True
                        break

                if nodeEvicted = False:                       # if a node was not evicted, then we move to the next node
                    curLevel-=1
                else:
                    break

        return result        # this can be optimized I believe
