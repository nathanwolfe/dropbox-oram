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
        self._C = maxStashSize
        
        self.use_vcache = True	
        self.debug = False			
        
		# TODO: wrap the common code (read/write paths and debug output)
		# Comment: You may find it helpful to print out stash content when debugging
		
		# TODO: support self.use_vcache = False (not urgent)
		
    def read(self, segID):
        reqResult = self._stash.request(segID)
        if reqResult != "not found" and self.use_vcache:
            #print("request succeeded")
            self._stash.addNode(reqResult)
            return reqResult.getData()
        else:
            leaf = self._posMap.lookup(segID)
            if leaf == -1:
                #print("not found in posmap")
                leaf = self._tree.randomLeaf()		
            transfer = self._tree.readPath(leaf)
            readResult = b""                  # -1 means not found	# TODO: reading or deleting a non-existent block is arguably illegal. You can simply raise an error using assert
            if self.debug:
                print("\tReading from path ", leaf)
            for bucket in transfer:
                for block in bucket:
                    if self.debug:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    if block.getSegID() != 0:
                        if block.getSegID() == segID:
                            #print ("found block")
                            readResult = block.getData()
                            block.setLeaf(self._tree.randomLeaf())
                            self._posMap.insert(segID, block.getLeaf())
                        self._stash.addNode(block)
                        #print(block.getSegID())
                if self.debug:
                    print("")
            outPath = self._stash.evict(leaf)
            if self.debug:				
                print("\tWriting to path ", leaf)		
                for bucket in outPath:
                    for block in bucket:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    print("")
				
            self._tree.writePath(leaf, outPath)
            return readResult
        
    def write(self, segID, data):
        if self._stash.getSize() > self._C:              # background eviction
            # print("backEv")
            self.read(self._tree.randomLeaf())
        
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
            if leaf == -1:
                #print("not found in posmap")
                leaf = self._tree.randomLeaf()
            transfer = self._tree.readPath(leaf)
            if self.debug:
                print("\tReading from path ", leaf)
            for bucket in transfer:
                for block in bucket:
                    if self.debug:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    if block.getSegID() != 0:
                        if block.getSegID() == segID:
                            self._posMap.delete(segID)
                        else:
                            self._stash.addNode(block)
                            #print(block.getSegID())
                if self.debug:
                    print("")
            outPath = self._stash.evict(leaf)
            if self.debug:				
                print("\tWriting to path ", leaf)		
                for bucket in outPath:
                    for block in bucket:
                        print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                    print("")
				
            self._tree.writePath(leaf, outPath)
        #else:
            #print("request succeeded")
