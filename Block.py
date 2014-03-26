class Block:
    #self._leaf = 0
    #self._segID = "-1"         # I believe you cannot set default values for these
    #self._data = -1
    def __init__(self, leaf, segID, data):
        self._leaf = leaf
        self._segID = segID
        self._data = data
    def getLeaf(self):
        return self._leaf
    def setLeaf(self, leaf):
        self._leaf = leaf
    def getSegID(self):
        return self._segID
    def getData(self):
        return self._data
    def setData(self, data):
        self._data = data

x = Block(1,"Hello",3)

a = x.setLeaf(5)

print (x.getSegID())
