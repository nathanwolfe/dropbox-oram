import Util

class Stash:
    _nodes

    def __init__(self):
        _nodes = []
        
    def getSize(self):
        return len(_nodes)
    
    def addNode(self, block):
        _nodes.append(block)

    def deleteNode(self, index):
        del _nodes[index]

    def request(self, segID):
        

    def scanStash(self, leaf):            # returns list of possible nodes (indices)
        result = []
        for i in range(0, len(_nodes)):
            if _nodes[i].getTag() = leaf:
                result.append(i)
        return result    # will change this function
