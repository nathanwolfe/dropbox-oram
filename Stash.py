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
            result[i] = [Block.Block(0, 0, b"")] * self._z
        
        for node in self._nodes:                                  # put nodes in the list where 0th element is 0th level, etc.
            curLevel = Util.getMaxLevel(leaf, node.getLeaf())
            #treeNodeIter = 0
            nodeEvicted = False

            while curLevel > -1:
                #print ("another test")
                treeNodeIter=0
                for treeNodeIter in range(self._z):
                    #print (treeNodeIter)
                    #print (curLevel)
                    if result[curLevel][treeNodeIter].getSegID() == 0:
                        #print ("entering")
                        result[curLevel][treeNodeIter] = node       # puts the segID of the block in the first available space in the list
                        #print(node.getSegID())
                        self._nodes.remove(node)
                        nodeEvicted = True
                        break

                if nodeEvicted == False:                       # if a node was not evicted, then we move to the next node
                    #print ("enter")
                    curLevel-=1
                else:
                    break

        return result        # this can be optimized I believe
