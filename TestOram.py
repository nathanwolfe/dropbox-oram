import Oram
import UserFileSys
import random
import time
import os
import shutil
import cProfile

def TestBasic() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
        except :
            print( "[TestBasic] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            print( "TestBasic failed." )

        print(oram._stash.getSize())
    print( "TestBasic Passed." )

def TestRepeatRW() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    db = {}
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
            oram.write(key, 'v')
        except :
            print( "[TestRepeatRW] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            return
    

def TestGeneral() :
    
	# Check: The following parameter seems to trigger an assertion
	
    #random.seed(1)	# this guarantees we get the same random numbers, and thus same results on every run
					# Comment: When you fixed this bug, remove the previous line so you can test with random input again.
	
    oramsize = 101
    #minoramsize = 7
    z = 3
    maxStashSize = 3
    segSize = 100
    oram = Oram.Oram(oramsize, z, segSize, maxStashSize, 1.8, 2, 2.2)
    
    check  = {}
    numKeys = 1000
    numTests = 1000
    
    lastStashSize = 0
    currentStashSize = 0
	
    
	
    for key in range(1, numKeys) :                 # writes a "random" string to each key from 0 to N
        data = "v" + str(random.randint(1,1000))
        oram.write(key, data)
        check[key] = data	
		
        currentStashSize = oram._stash.getSize()
        #print ("ORAM Stash Size: ", currentStashSize)		
        if 	currentStashSize - lastStashSize > 1:
            print("Stash increases by more than 1")			
            exit(0)
        lastStashSize = currentStashSize			
        
    for i in range(0, numTests):        # does a random operation
        operation = random.random()
        key = random.randint(1, numKeys-1)
        # if ((operation * 10) % 1 < .1):
        #     oram.grow(2)
        #     oramsize += 2
        # elif ((operation * 10) % 1 < .2 and oramsize > minoramsize):
        #     oram.shrink(2)
        #     oramsize -= 2
        if (operation < .2):
            data = "x" + str(random.randint(1,1000))
            oram.write(key, data)
            check[key] = data

        elif (operation <.6):
            if (check[key] != ""):
                try:
                    getValue = oram.read(key).decode("utf-8")	
                    assert (getValue == check[key])
                except:
                    print( "[TestGeneral] key=%d. expecting %s but got %s" % (key, check[key], getValue) )
                    return

        else:
            if (check[key] != ""):
                oram.delete(key)
                check[key] = ""
        
        currentStashSize = oram._stash.getSize()
        #print ("ORAM Stash Size: ", currentStashSize)		
        # if currentStashSize - lastStashSize > 1:
        #     print("Stash increases by more than 1")			
        #     exit(0)
            
        lastStashSize = currentStashSize
        
    print("final stash size:", currentStashSize)
    print("TestGeneral Passed")

def TestBackEv():
    oramsize = 4095
    segSize = 100
    z = 2
    
    #numKeys = 64
    #numTests = 10000
    
    print ("z = " + str(z) + ", oram size = " + str(oramsize))
    numKeys = int(oramsize*z / 2)
    for maxStashSize in range(5, 50, 5):
        oram = Oram.Oram(oramsize, z, segSize, maxStashSize, 1.8, 2.0, 2.2)
        numBackEv = 0
        for key in range(1, numKeys+1) :                 # writes a "random" string to each key from 0 to N
            while (oram._stash.getSize() > oram._c):
                oram.access("backEv", 0, None)
                #print ("backEv")
                numBackEv+=1
            data = "v" + str(random.randint(1,1000))
            oram.write(key, data)			
        
        for i in range (oramsize*2):
            key = i%numKeys + 1
            while (oram._stash.getSize() > oram._c):
                oram.access("backEv", 0, None)
                numBackEv+=1
            oram.read(key)

        print ("\tMax Stash Size = " + str(maxStashSize) + ": dummy- " + str(numBackEv) + ", actual- " + str(2*oramsize + numKeys))
        print ("\t\tRatio = " + str(numBackEv / (2*oramsize + numKeys)))

def ORAMvsNormal():
    from os.path import expanduser
    home = expanduser("~")

    oram = UserFileSys.UserFileSys(3, 3, 4096, 10, 1.8, 2.0, 2.2)
    total = 0
    numTests = 100
    fileName = "Birds.jpg"
    for i in range(numTests):
        start = time.clock()
        oram.write(fileName)
        oram.read(fileName)
        oram.delete(fileName)
        timeTaken = time.clock() - start
        #print(timeTaken)
        #print(oram._Oram._tree.getSize())
        
        total += timeTaken

    avg = total / numTests
    print ("Average time taken with ORAM for file " + fileName + ": " + str(avg))

    """total = 0
    for i in range(numTests):
        start = time.clock()
        shutil.copyfile(fileName, home + "/Dropbox/test.MPG")
        total += (time.clock()-start)
    avg = total/numTests
    print ("Average time taken without ORAM for file " + fileName + ": " + str(avg))
    """
def TestSegSize():
    fileName = "Zou- Mathematics Solutions.pdf"
    numTests = 100
    segSize = 1024
    while segSize <= 33000:
        total = 0
        oram = UserFileSys.UserFileSys(101, 3, segSize, 10, 1.8, 2.0, 2.2)
        for i in range(numTests):
            start = time.clock()
            oram.write(fileName)
            oram.read(fileName)
            oram.delete(fileName)
            timeTaken = time.clock() - start
            total+=timeTaken
        avg = total / numTests
        print(str(segSize) + " " + str(avg))
        segSize *= 2

def TestMultiBlock():
    fileName = "Zou- Mathematics Solutions.pdf"
    numTrials = 1000
    numTests = 5
    for i in range(2, numTests+1):
        total = 0
        oram = UserFileSys.UserFileSys(101, 3, 4096, 10, 1.8, 2.0, 2.2, i)
        for j in range(numTrials):
            start = time.clock()
            oram.write(fileName)
            oram.read(fileName)
            oram.delete(fileName)
            timeTaken = time.clock() - start
            total+=timeTaken
        avg = total / numTrials
        print(str(i) + ": " + str(avg))  
        
    
#TestBasic()
#TestRepeatRW()
#TestGeneral()
#TestBackEv()
#cProfile.run('ORAMvsNormal()')
#ORAMvsNormal()
#TestSegSize()
TestMultiBlock()        
