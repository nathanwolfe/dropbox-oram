import Oram
import DBFileSys

class UserFileSys:
    def __init__(self, treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR):
        self._oram = Oram.Oram(treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR)
        self._segSizeMap = {}          # holds number of segments in file
        self._segIDMap = {}         # holds segIDs of the file segments
        self._segSize = segSize
        self._curSegID = 1

        self.useMultiBlock = True
        self.debug = False

    def write(self, userFileName):
        readFile = open(userFileName, "rb")
        segNum = 0
        if self.useMultiBlock:
            segIDList = []
            dataList = []
        while True:
            # Same thing here. Read in the entire file once and then process it.
            dataSeg = readFile.read(self._segSize)
            if not dataSeg:
                break            # break the loop once end of file is reached

            if self.debug:
                print ("segName: " + str(userFileName + "_" + str(segNum)))
            
            # An optimization: map filename to a list of segIDs. I mean filename --> [ID1, ID2, ID3 ...] 
            # No need for filename1, filename2, ...
            # Two benefits. First, this saves some space.
            # Second, you don't need to increment curSegID segNum multiple times. 
            # You know from the beginning how large the file is and how many chunks you need. 
            
            self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
            if self.useMultiBlock:
                segIDList.append(self._curSegID)
                dataList.append(dataSeg)
            else:
                self._oram.write(self._segIDMap[userFileName + "_" + str(segNum)], dataSeg)
            self._curSegID += 1
            segNum += 1
        if self.useMultiBlock:
            self.writeList(segIDList, dataList)

        self._segSizeMap[userFileName] = segNum
        readFile.close()

    def read(self, userFileName):
        if userFileName in self._segSizeMap:
            numSegments = self._segSizeMap[userFileName]
            if self.useMultiBlock:
                segIDList = []
                for segNum in range(numSegments):
                    segIDList.append(self._segIDMap[userFileName + "_" + str(segNum)])
                return self.readList(segIDList)
            else:
                result = b""
                for segNum in range(numSegments):
                    if self.debug:
                        print ("READING FILE " + str(self._segIDMap[userFileName + "_" + str(segNum)]))
                        print (self._oram.read(self._segIDMap[userFileName + "_" + str(segNum)]))
                    result += self._oram.read(self._segIDMap[userFileName + "_" + str(segNum)])
                return result

        else:
            print ("Reading nonexistent file...")

    def delete(self, userFileName):
        if userFileName in self._segSizeMap:
            numSegments = self._segSizeMap[userFileName]
            if self.useMultiBlock:
                segIDList = []
            for segNum in range(numSegments):
                if self.useMultiBlock:
                    segIDList.append(self._segIDMap[userFileName + "_" + str(segNum)])
                else:
                    self._oram.delete(self._segIDMap[userFileName + "_" + str(segNum)])
                del self._segIDMap[userFileName + "_" + str(segNum)]
            if self.useMultiBlock:
                self.deleteList(segIDList)
        
            del self._segSizeMap[userFileName]

        else:
            print ("Deleting nonexistent file...")

    def writeList(self, segIDList, dataList):
        while segIDList != []:
            dataList = self._oram.multiWrite(segIDList, dataList)
            segIDList = [segIDList[i] for i in range(len(segIDList)) if dataList[i] is not None]
            dataList = [x for x in dataList if x is not None]

    def readList(self, segIDList):
        result = [None] * len(segIDList)
        while segIDList != []:
            dataList = self._oram.multiRead(segIDList)
            counter = 0
            for i in range(len(result)):
                if result[i] == None:
                    print(len(dataList), counter, i)
                    result[i] = dataList[counter]
                    counter += 1
            segIDList = [segIDList[i] for i in range(len(segIDList)) if result[i] is None]
        return b"".join(result)

    def deleteList(self, segIDList):
        while segIDList != []:
            dataList = self._oram.multiDelete(segIDList)
            segIDList = [segIDList[i] for i in range(len(segIDList)) if dataList[i] is None]
            
    def writeEverything(self):
        DBFileSys.writeStash(self._oram.getStash().getNodes(), self._segSize)     # I shouldn't access private member variables right?
        DBFileSys.writeDictionary("posMap", self._oram.getPosMap().getMap())
        DBFileSys.writeDictionary("segSizeMap", self._segSizeMap)
        DBFileSys.writeDictionary("segIDMap", self._segIDMap)

    def readEverything(self):
        if DBFileSys.readStash(self._segSize) == "new ORAM":    # if the files don't exist yet, then write everything
            self.writeEverything()
            self.readEverything()
            print ("New ORAM Created")
        else:
            self._oram.setStash(DBFileSys.readStash(self._segSize))
            self._oram.setPosMap(DBFileSys.readDictionary("posMap"))
            self._segSizeMap = DBFileSys.readDictionary("segSizeMap")
            self._segIDMap = DBFileSys.readDictionary("segIDMap")

"""test = UserFileSys(101, 3, 3000, 10, 1.8, 2.0, 2.2)
test.write("Birds.jpg")
test.writeEverything()
test.readEverything()
#print("checkpoint1")
pic = test.read("Birds.jpg")
#print ("checkpoint")
output = open("file.jpg", "wb")
output.write(pic)
output.close()"""
