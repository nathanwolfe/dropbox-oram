import Oram
import DBFileSys

class UserFileSys:
    def __init__(self, treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR, multiBlock):
        self._oram = Oram.Oram(treeSize, z, segSize, maxStashSize, growR, targetR, shrinkR)
        self._segSizeMap = {}          # filename -> number segments in file
        self._segIDMap = {}         # filename + segNum -> segID
        self._blockSpaceLeft = {}   # segID -> amount of space left in block
        self._startEnd = {}         # segID (of a "mini" segment) -> start and end offsets
        self._segSize = segSize
        self._curSegID = 1

        self.multiBlock = multiBlock         # size of multiblock group (1 for no optimization)
        self.blockPack = False
        self.debug = False


    def write(self, userFileName):
        readFile = open(userFileName, "rb")

        if not self.blockPack:
            segNum = 0
            segIDList = []
            dataList = []
            while True:
                # Same thing here. Read in the entire file once and then process it.
                dataSeg = readFile.read(self._segSize)
                if not dataSeg:
                    break            # break the loop once end of file is reached

                if len(segIDList) == self.multiBlock:
                    self._oram.multiWrite(segIDList, dataList)
                    segIDList = []
                    dataList = []

                if self.debug:
                    print ("segName: " + str(userFileName + "_" + str(segNum)))
                
                # An optimization: map filename to a list of segIDs. I mean filename --> [ID1, ID2, ID3 ...] 
                # No need for filename1, filename2, ...
                # Two benefits. First, this saves some space.
                # Second, you don't need to increment curSegID segNum multiple times. 
                # You know from the beginning how large the file is and how many chunks you need. 
                
                self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
                
                segIDList.append(self._curSegID)
                dataList.append(dataSeg)

                self._curSegID += 1
                segNum += 1

            self._oram.multiWrite(segIDList, dataList)

            self._segSizeMap[userFileName] = segNum

        else:             # only works with autoresize for now
            allData = readFile.read()
            numSeg = (int)(len(allData)/self._segSize) + 1
            segIDList = []
            dataList = []
            curPosition = 0
            
            for segNum in range(numSeg):
                packed = False
                dataSeg = allData[curPosition:curPosition+self._segSize]

                if segNum == numSeg-1:       # we are at the last segment
                    print(self._blockSpaceLeft)
                    for key, spaceLeft in self._blockSpaceLeft.items():
                        if len(dataSeg) <= spaceLeft:
                            #print("entered")
                            lastSegID = key
                            print("packed segID: " + str(lastSegID))
                            b"".join([dataSeg,self._oram.read(lastSegID)])   # **** not sure about this ****
                            self._segIDMap[userFileName + "_" + str(segNum)] = lastSegID
                            #print (userFileName + "_" + str(segNum))
                            
                            segIDList.append(lastSegID)
                            dataList.append(dataSeg)

                            start = self._segSize - self._blockSpaceLeft[lastSegID] + 1
                            self._startEnd[lastSegID] = [start, start + len(dataSeg)] # do something about start and end offsets
                            
                            self._blockSpaceLeft[lastSegID] -= len(dataSeg)
                            packed = True
                            break

                    if packed == False:
                        #print("unpacked segID: " + str(self._curSegID))
                        # if there are no available ones, we map it to a new segID
                        self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
                        #print(userFileName + "_" + str(segNum))
                        segIDList.append(self._curSegID)
                        dataList.append(dataSeg)

                        self._startEnd[self._curSegID] = [0, len(dataSeg)]
                        self._blockSpaceLeft[self._curSegID] = self._segSize - len(dataSeg)
                        #print(len(self._blockSpaceLeft))
                        self._curSegID += 1

                            #start and end offsets
                            
                else:                 # write the block normally
                    self._segIDMap[userFileName + "_" + str(segNum)] = self._curSegID
                    segIDList.append(self._curSegID)
                    dataList.append(dataSeg)
                    self._curSegID += 1
                    curPosition += self._segSize

                    if len(segIDList) == self.multiBlock:
                        print("test")
                        self._oram.multiWrite(segIDList, dataList)
                        segIDList = []
                        dataList = []

            self._oram.multiWrite(segIDList, dataList)

            self._segSizeMap[userFileName] = numSeg

                    
        readFile.close()

    def read(self, userFileName):
        if not self.blockPack:
            if userFileName in self._segSizeMap:
                numSegments = self._segSizeMap[userFileName]
                segIDList = []
                result = b""
                for segNum in range(numSegments):
                    if len(segIDList) == self.multiBlock:
                        result += b"".join(self._oram.multiRead(segIDList))
                        segIDList = []
                    segIDList.append(self._segIDMap[userFileName + "_" + str(segNum)])
                result += b"".join(self._oram.multiRead(segIDList))
                return result

            else:
                print ("Reading nonexistent file...")

        else:
            if userFileName in self._segSizeMap:
                numSegments = self._segSizeMap[userFileName]
                segIDList = []
                result = b""
                for segNum in range (numSegments):
                    if segNum == numSegments-1:
                        lastSegID = self._segIDMap[userFileName + "_" + str(segNum)]
                        start, end = self._startEnd[lastSegID]
                        lastDataBlock = self._oram.read(lastSegID)
                        lastDataSeg = lastDataBlock[start:end]
                        
                        #look up the segID of the last segment
                    else:
                        if len(segIDList) == self.multiBlock:
                            result+= b"".join(self._oram.multiRead(segIDList))
                            segIDList = []
                        segIDList.append(self._segIDMap[userFileName + "_" + str(segNum)])

                if segIDList != []:
                    result += b"".join(self._oram.multiRead(segIDList))

                result += lastDataSeg         #idk if this is ok....
                return result
                    

            else:
                print ("Reading nonexistent file...")

    def delete(self, userFileName):
        if userFileName in self._segSizeMap:
            numSegments = self._segSizeMap[userFileName]
            segIDList = []
            for segNum in range(numSegments):
                if len(segIDList) == self.multiBlock:
                    self._oram.multiDelete(segIDList)
                    segIDList = []
                segIDList.append(self._segIDMap[userFileName + "_" + str(segNum)])
                del self._segIDMap[userFileName + "_" + str(segNum)]
            self._oram.multiDelete(segIDList)
            del self._segSizeMap[userFileName]

        else:
            print ("Deleting nonexistent file...")
            
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

"""test = UserFileSys(101, 3, 3000, 10, 1.8, 2.0, 2.2, 1)
test.write("Birds.jpg")
test.writeEverything()
test.readEverything()
#print("checkpoint1")
pic = test.read("Birds.jpg")
#print ("checkpoint")
output = open("file.jpg", "wb")
output.write(pic)
output.close()"""
