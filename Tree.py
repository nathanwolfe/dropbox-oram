# nodes are stored in a list
# their position in the list is their address - 1
# paths on the tree go from leaf to root
# readPath and writePath use 2d lists of blocks

import random
import Util
import Block

class Tree:
    def __init__(self, nodeNumber, z):
        self._nodes = [0] * nodeNumber
        for i in range(nodeNumber):
            self._nodes[i] = _TreeNode(z)
    def getSize(self):
        return len(self._nodes)
    def randomLeaf(self):
        return random.randint(int(len(self._nodes) / 2) + 1, len(self._nodes))
    def readPath(self, leaf):
        result = []
        for addr in Util.getPathNodes(leaf):
            result.append(self._nodes[addr - 1].read())
        return result
    def writePath(self, leaf, blocks):
        for addr in Util.getPathNodes(leaf):
            self._nodes[addr-1].write(blocks[0])
            blocks.pop(0)

class _TreeNode:
    def __init__(self, z):
        self._blocks = [0] * z
        for i in range(z):
            self._blocks[i] = Block.Block(0, -1, -1)
    def read(self):
        return self._blocks
    def write(self, blocks):
        self._blocks = blocks
