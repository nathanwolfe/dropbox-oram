import StashNode

class Stash:
    _nodes

    def _init_(self):
        _nodes = []
        
    def getSize(self):
        return len(_nodes)
    
    def addNode(self, stashNode):    # do i need to specify that stashNode is a _stashNode object?
        _nodes.append(stashNode)

    def deleteNode(self, index):
        del _nodes[index]

    def scanStash(self, leaf):            # returns list of possible nodes (indices)
        result = []
        for i in range(0, len(_nodes)):
            if _nodes[i].getTag() = leaf:
                result.append(i)
        return result

# where to return the actual data when operation is read?
# also, how to add a node to the stash from the tree? convert treeNode to stashNode?
