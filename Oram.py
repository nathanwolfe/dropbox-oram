import Util
import Block
import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z, segmentSize, maxStashSize, growR, targetR, shrinkR): # grow/shrink triggered by ratio (buckets * z) / (# of segments)
        self._z = z
        self._tree = Tree.Tree(treeSize, z, segmentSize)
        self._stash = Stash.Stash(z)
        self._posMap = PosMap.PosMap()
        self._c = maxStashSize

        self._growR = growR
        self._targetR = targetR
        self._shrinkR = shrinkR

        self._segCounter = 0

        self.autoResize = True
        self.showResize = False

        self.useVCache = True
        self.debug = False			
        
		# Comment: You may find it helpful to print out stash content when debugging
		
    def access(self, action, segID, data):		
		# Comment: also need back ground eviction on a read operation       
		# TODO: try to get the background eviction rate under different Z and tree size
        while (action == "read" or action == "write") and self._stash.getSize() > self._c:              # background eviction
            if self.debug:
                print("backEv")
            self.access("backEv", 0, None)

        if self.autoResize == True and self._segCounter != 0:
            currentR = (self._tree.getSize() * self._z) / self._segCounter
            if currentR < self._growR:
                self.grow(int(((self._targetR - currentR) * self._segCounter) / self._z))
            elif currentR > self._shrinkR:
                self.shrink(int(((currentR - self._targetR) * self._segCounter) / self._z))
        
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
            else:
                self._posMap.delete(segID)
                self._segCounter -= 1
            if self.useVCache == False:
                self.treeAccess("dummy", segID, data)
            return reqResult.getData()
        else:
            return self.treeAccess(action, segID, data)

    def treeAccess(self, action, segID, data):
        leaf = self._posMap.lookup(segID)
        if leaf == -1:
            assert ((action == "write" and segID > 0) or action == "backEv" or action == "dummy"), "tried to " + action + " nonexistent segID"
            leaf = self._tree.randomLeaf()
        transfer = self._tree.readPath(leaf)
        result = b""
        if self.debug:
                print("\treading from path ", leaf)
        
        for bucket in transfer:
            for block in bucket:
                if self.debug:
                    print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                if block.getSegID() != 0:
                    if block.getSegID() == segID:
                        result = block.getData()
                        if action == "write":
                            block.setData(data)
                        if action == "read" or action == "write":
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        if action != "delete":
                            self._stash.addNode(block)
                        else:
                            self._posMap.delete(segID)
                            self._segCounter -= 1
                    else:
                        block.setLeaf(self._posMap.lookup(block.getSegID()))
                        self._stash.addNode(block)
            if self.debug:
                print("")
                    
        if result == b"" and action == "write":
            newBlock = Block.Block(self._tree.randomLeaf(), segID, data)
            self._stash.addNode(newBlock)
            self._posMap.insert(segID, newBlock.getLeaf())
            self._segCounter += 1
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
        if numLeaves == 0:
            return None
        assert (numLeaves > 0), "illegal growth amount"
        if numLeaves % 2 == 1:
            numLeaves -= 1
        if self.showResize:
            print("growing by", numLeaves)
        self._tree.grow(numLeaves)
        self._stash.correctLeaves(self._tree.getSize())
        self._posMap.correctLeaves(self._tree.getSize())

    def shrink(self, numLeaves):
        if numLeaves == 0:
            return None
        assert (numLeaves > 0), "illegal shrinkage amount"
        if numLeaves % 2 == 1:
            numLeaves -= 1
        if self.showResize:
            print("shrinking by", numLeaves)
        dump = self._tree.shrink(numLeaves)
        for block in dump:
            if block.getSegID() != 0:
                self._stash.addNode(block)
        self._stash.correctLeaves(self._tree.getSize())
        self._posMap.correctLeaves(self._tree.getSize())

    def setPosMap(self, dictionary):
        self._posMap.setMap(dictionary)

    def getPosMap(self):
        return self._posMap

    def setStash(self, nodes):
        self._stash.setNodes(nodes)

    def getStash(self):
        return self._stash
