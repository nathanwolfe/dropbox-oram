import Util
import Block
import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z, segmentSize):
        self._z = z
        self._tree = Tree.Tree(treeSize, z, segmentSize)
        self._stash = Stash.Stash(z)
        self._posMap = PosMap.PosMap()	
        self.use_vcache = True
		
        self.debug = True			
        
    def read(self, segID):
        reqResult = self._stash.request(segID)
        if reqResult != "not found" and self.use_vcache:
            #print("request succeeded")
            self._stash.addNode(reqResult)
            return reqResult.getData()
        else:
            leaf = self._posMap.lookup(segID)
            transfer = self._tree.readPath(leaf)
            readResult = b""                          # -1 means not found
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID() != 0:
                        if block.getSegID() == segID:
                            #print ("found block")
                            readResult = block.getData()
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        self._stash.addNode(block)
                        #print(block.getSegID())
            self._tree.writePath(leaf, self._stash.evict(leaf))
            return readResult
        
    def write(self, segID, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        reqResult = self._stash.request(segID)
        if reqResult != "not found" and self.use_vcache:
            #print("request succeeded")
            reqResult.setData(data)
            self._stash.addNode(reqResult)
        else:
            leaf = self._posMap.lookup(segID)
            if leaf == -1:
                #print("not found in posmap")
                leaf = self._tree.randomLeaf()
            transfer = self._tree.readPath(leaf)
            blockFound = False
			
            if self.debug:
                print("\tReading from path ", leaf)			
            for bucket in transfer:          				
                for block in bucket:
                    if self.debug:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())								
                    if block.getSegID() != 0:
                        if block.getSegID() == segID:
                            blockFound = True
                            block.setData(data)
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        self._stash.addNode(block)
                        #print(block.getSegID())
                if self.debug:
                    print("")
					
            if blockFound == False:
                newBlock = Block.Block(self._tree.randomLeaf(), segID, data)
                self._stash.addNode(newBlock)
                self._posMap.insert(segID, newBlock.getLeaf())
                #print("new block inserted")

            outPath = self._stash.evict(leaf)
            if self.debug:				
                print("\tWriting to path ", leaf)		
                for bucket in outPath:
                    for block in bucket:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    print("")
				
            self._tree.writePath(leaf, outPath)
            
    def delete(self, segID):
        reqResult = self._stash.request(segID)
        if reqResult == "not found":
            leaf = self._posMap.lookup(segID)
            transfer = self._tree.readPath(leaf)
            for bucket in transfer:
                for block in bucket:
                    if block.getSegID() != 0:
                        if block.getSegID() == segID:
                            self._posMap.delete(segID)
                        else:
                            self._stash.addNode(block)
                            #print(block.getSegID())
            self._tree.writePath(leaf, self._stash.evict(leaf))
        #else:
            #print("request succeeded")
