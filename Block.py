class Block:
    _addr = 0
    _tag = -1
    _data = -1
    def __init__(self, addr, tag, data):
        _addr = addr
        _tag = tag
        _data = data
    def getAddr(self):
        return _addr
    def setAddr(self, addr):
        _addr = addr
    def getTag(self):
        return _tag
    def getData(self):
        return _data
    def setData(self, data):
        _data = data
