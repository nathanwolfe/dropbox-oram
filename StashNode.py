import Block

class _StashNode:
    _block
    def __init__(self, addr, tag, data):
        _block = Block(addr, tag, data)

    def getAddr(self):
        return _block.getAddr()
    def setAddr(self, addr):
        _block.setAddr(addr)
        
    def getTag(self):
        return _block.getTag()    # is setTag not necessary here?

    def getData(self):
        return _block.getData()
    def setData(self, data):
        _block.setData(data)
