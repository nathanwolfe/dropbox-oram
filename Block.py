class Block:
    
    def __init__(self, leaf, segID, data):
        self._leaf = leaf
        self._segID = segID
        self._data = data
        
    def getLeaf(self):
        return self._leaf
    
    def setLeaf(self, leaf):
        self._leaf = leaf
        return self.getLeaf()
        
    def getSegID(self):
        return self._segID
    
    def getData(self):
        return self._data
    
    def setData(self, data):
        self._data = data
