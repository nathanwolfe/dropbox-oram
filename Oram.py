import Util
import Block
import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z):
        _z = z
        self._tree = Tree.Tree(treeSize, z)
        self._stash = Stash.Stash()
        self._posMap = PosMap.PosMap()
    def read(self, segID):
        reqResult = _stash.request(segID, "read", 0)
        if reqResult != "not found":
            return reqResult
        else:
            leaf = _posMap.lookup(segID)
            transfer = _tree.readPath(leaf)
            readResult = -1 # -1 means not found
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1:
                        if block.getSegID == segID:
                            readResult = block.getData()
                            block.setLeaf(_tree.randomLeaf())
                            _posMap.insert(segID, block.getLeaf())
                        _stash.addNode(block)
            _tree.writePath(leaf, _stash.evict(leaf))
            return readResult
    def write(self, segID, data):
        reqResult = _stash.request(segID, "write", data)
        if reqResult == "not found":
            leaf = _posMap.lookup(segID)
            transfer = _tree.readPath(leaf)
            blockFound = False
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1:
                        if block.getSegID == segID:
                            blockFound = True
                            block.setData(data)
                            block.setLeaf(_tree.randomLeaf())
                            _posMap.insert(segID, block.getLeaf())
                        _stash.addNode(block)
            if !blockFound:
                newBlock = Block.Block(_tree.randomLeaf(), segID, data)
                _stash.addNode(newBlock)
                _posMap.insert(segID, newBlock.getLeaf())
            _tree.writePath(leaf, _stash.evict(leaf))
    def delete(self, segID):
        reqResult = _stash.request(segID, "delete", 0)
        if reqResult == "not found":
            leaf = _posMap.lookup(segID)
            transfer = tree.readPath(leaf)
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID != -1 and block.getSegID != segID:
                        _stash.addNode(block)
            _tree.writePath(leaf, _stash.evict(leaf))
