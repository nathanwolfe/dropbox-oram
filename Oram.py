import Util
import Block
import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z, segmentSize, maxStashSize):
        self._z = z
        self._tree = Tree.Tree(treeSize, z, segmentSize)
        self._stash = Stash.Stash(z)
        self._posMap = PosMap.PosMap()
        self._c = maxStashSize
        
        self.useVCache = True	
        self.debug = False			
        
		# Comment: You may find it helpful to print out stash content when debugging
		
    def access(self, action, segID, data):		
		# Comment: also need back ground eviction on a read operation       
		# TODO: try to get the background eviction rate under different Z and tree size	
        while action == "write" and self._stash.getSize() > self._c:              # background eviction
            if self.debug:
                print("backEv")
            self.access("backEv", 0, None)
        if isinstance(data, str):
            data = data.encode("utf-8")
        reqResult = self._stash.request(segID)
        if reqResult != "not found":
			# TODO: maintain some statistics on the hit rate of this optimization		
            if self.debug:
                print("found in stash")
            if action == "write":
                reqResult.setData(data)
            if action != "delete":
                self._stash.addNode(reqResult)
            if self.useVCache == False:
                self._posMap.insert(0, reqResult.getLeaf())
                self.read(0)
                self._posMap.delete(0)
            return reqResult.getData()
        else:
            leaf = self._posMap.lookup(segID)
            if leaf == -1:
                assert ((action == "write" and segID > 0) or action == "backEv"), "tried to " + action + " nonexistent segID"
                leaf = self._tree.randomLeaf()
            transfer = self._tree.readPath(leaf)
            result = b""
            if self.debug:
                print("\treading from path ", leaf)
					
			# Comment: may be cleaner to put this in a function like readPath()
            for bucket in transfer:
                for block in bucket:
                    if self.debug:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    if block.getSegID() != 0:
                        newLeaf = Util.correctLeaf(block.getLeaf(), self._tree.getSize())
                        if newLeaf != None:
                            block.setLeaf(newLeaf)
                        if block.getSegID() == segID:
                            result = block.getData()
                            if action == "write":
                                block.setData(data)
                            if action != "delete":
                                block.setLeaf(self._tree.randomLeaf())
                                self._posMap.insert(segID, block.getLeaf())
                                self._stash.addNode(block)
                            else:
                                self._posMap.delete(segID)
                        else:
                            self._stash.addNode(block)
                if self.debug:
                    print("")
			
            if result == b"" and action == "write":
                newBlock = Block.Block(self._tree.randomLeaf(), segID, data)
                self._stash.addNode(newBlock)
                self._posMap.insert(segID, newBlock.getLeaf())
                if self.debug:
                    print("new block inserted")
            outPath = self._stash.evict(leaf)
            if self.debug:
                print("\twriting to path", leaf)
                for bucket in outPath:
                    for block in bucket:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    print("")
            self._tree.writePath(leaf, outPath)
            return result

    def read(self, segID):
        return self.access("read", segID, None)

    def write(self, segID, data):
        self.access("write", segID, data)

    def delete(self, segID):
        self.access("delete", segID, None)

    def grow(self, numLeaves):
        assert (numLeaves > 0 and numLeaves % 2 == 0), "illegal growth amount"
        self._tree.grow(numLeaves)
        self._stash.correctLeaves(self._tree.getSize())
        self._posMap.correctLeaves(self._tree.getSize())
