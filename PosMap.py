import Util

class PosMap :

    def __init__(self):
        self._posMap = {}

    def lookup(self, key) :
        if not key in self._posMap:
            return -1
        return self._posMap[key]

    def insert(self, key, value):
        self._posMap[key] = value

    def delete(self, key):
        del self._posMap[key]

    def correctLeaves(self, treeSize):
        for key in self._posMap:
            newLeaf = Util.correctLeaf(self._posMap[key], treeSize, key % 2)
            if newLeaf != None:
                self._posMap[key] = newLeaf
