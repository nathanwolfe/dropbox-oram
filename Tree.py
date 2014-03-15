# nodes are stored in a list
# their position in the list is their address - 1
# paths on the tree go from leaf to root
# read and write use 2d lists of blocks

class Tree:
    _nodes = []
    def __init__(self, nodeNumber, z):
        _nodes = [0] * nodeNumber
        for i in range(nodeNumber):
            _nodes[i] = _TreeNode(z)
    def getSize(self):
        return len(_nodes)
    def pathAddrs(self, leaf):
        result = []
        while (leaf > 0):
            result.append(leaf)
            leaf = int(leaf / 2)
        return result
    def read(self, leaf):
        result = []
        for addr in pathAddrs(leaf):
            result.append(_nodes[addr - 1].read())
        return result
    def write(self, leaf, blocks):
        for addr in pathAddrs(leaf):
            _nodes[addr-1].write(blocks[0])
            blocks.pop(0)

class _TreeNode:
    _blocks = []
    def __init__(self, z):
        _blocks = [0] * z
        for i in range(z):
            _blocks[i] = Block(0, -1, -1)
    def read(self):
        return _blocks
    def write(self, blocks):
        _blocks = blocks
