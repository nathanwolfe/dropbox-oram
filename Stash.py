import Util
import Block

class Stash:

    def __init__(self, z):
        self._nodes = []
        self._z = z
        
    def getSize(self):
        return len(self._nodes)
    
    def addNode(self, block):
        self._nodes.append(block)

    def deleteNode(self, index):
        del self._nodes[index]

    def request(self, segID):
        
        for i in range(len(self._nodes)):
            if self._nodes[i].getSegID() == segID:
                return self._nodes.pop(i)                # request just returns the node if found
                       
        return "not found"

    def evict(self, leaf):            # returns list of the blocks that go in each node on the path as a 2d list, should compare IDs and return if found as well
        numLevels = Util.levelNumber(leaf) + 1           # in which file would I find these?
        result = [0] * numLevels
        
        for i in range(numLevels):
            result[i] = [Block.Block(0, -1, -1)] * self._z
        
        for i in range(len(self._nodes)):                                  # put nodes in the list where 0th element is 0th level, etc.
            curLevel = Util.getMaxLevel(leaf, self._nodes[i].getLeaf())
            treeNodeIter = 0
            nodeEvicted = False

            while curLevel > -1:
                for treeNodeIter in range(self._z):
                    if result[curLevel][treeNodeIter] == -1:
                        result[curLevel][treeNodeIter] = self._nodes[i]       # puts the segID of the block in the first available space in the list
                        self.deleteNode(i)
                        nodeEvicted = True
                        break

                if nodeEvicted == False:                       # if a node was not evicted, then we move to the next node
                    curLevel-=1
                else:
                    break

        return result        # this can be optimized I believe
