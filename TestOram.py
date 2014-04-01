import Oram
import random

def TestBasic() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4)
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key)
            assert (getvalue == str(key))
        except :
            print( "[TestBasic] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            print( "TestBasic failed." )
    print( "TestBasic Passed." )

def TestRepeatRW() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4)
    db = {}
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key)
            assert (getvalue == str(key))
            oram.write(key, 'v')
        except :
            print( "[TestRepeatRW] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            return
    

def TestGeneral() :
    oramsize=1024*1024 - 1
    oram = Oram.Oram(oramsize, 4)
    check  = {}

    numTests = 1000
    for key in range(0, numTests) :                 # writes a "random" string to each key from 0 to numTests-1
        data = "v" + str(random.randint(1,1000))
        oram.write(key, data)
        check[key] = data
        
    for key in range(0, numTests):        # deletes a randomn subset of them  
        delete  = random.random()
        if (delete<0.4):
            oram.delete(key)
            check[key] = -1

    for key in range(0,numTests):        # actual test
        try:
            getValue = oram.read(key)
            assert (getValue == check[key])
            
        except:
            print( "[TestGeneral] key=%d. expecting %s but got %s" % (key, check[key], getvalue) )
            return
        
    print ("TestGeneral Passed")

#TestBasic()
# TestRepeatRW()
TestGeneral()
