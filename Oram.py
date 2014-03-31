import Util
import Block
import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z):
        self._z = z
        self._tree = Tree.Tree(treeSize, z)
        self._stash = Stash.Stash(z)
        self._posMap = PosMap.PosMap()
        
    def read(self, segID):
        reqResult = self._stash.request(segID)
        if reqResult != "not found":
            self._stash.addNode(reqResult)
            return reqResult.getData()
        else:
            leaf = self._posMap.lookup(segID)
            transfer = self._tree.readPath(leaf)
            readResult = -1                          # -1 means not found
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1:
                        if block.getSegID == segID:
                            readResult = block.getData()
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        self._stash.addNode(block)
            self._tree.writePath(leaf, self._stash.evict(leaf))
            return readResult
        
    def write(self, segID, data):
        reqResult = self._stash.request(segID)
        if reqResult != "not found":
            reqResult.setData(data)
            self._stash.addNode(reqResult)
        else:
            leaf = self._posMap.lookup(segID)
            transfer = self._tree.readPath(leaf)
            blockFound = False
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1:
                        if block.getSegID == segID:
                            blockFound = True
                            block.setData(data)
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        self._stash.addNode(block)
            if blockFound == False:
                newBlock = Block.Block(self._tree.randomLeaf(), segID, data)
                self._stash.addNode(newBlock)
                self._posMap.insert(segID, newBlock.getLeaf())
            self._tree.writePath(leaf, self._stash.evict(leaf))
            
    def delete(self, segID):
        reqResult = self._stash.request(segID)
        if reqResult == "not found":
            leaf = self._posMap.lookup(segID)
            transfer = tree.readPath(leaf)
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1:
                        if block.getSegID == segID:
                            self._posMap.delete(segID)
                        else:
                            self._stash.addNode(block)
            self._tree.writePath(leaf, self._stash.evict(leaf))
