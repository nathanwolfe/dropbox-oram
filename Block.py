class Block:
    _leaf = 0
    _segID = -1
    _data = -1
    def __init__(self, leaf, segID, data):
        self._leaf = leaf
        self._segID = segID
        self._data = data
    def getLeaf(self):
        return _leaf
    def setLeaf(self, leaf):
        _leaf = leaf
    def getTag(self):
        return _segID
    def getData(self):
        return _data
    def setData(self, data):
        _data = data
