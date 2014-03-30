import Oram

def TestBasic() :
    oram = Oram.Oram(7, 4)
    for key in range(0, 7) :
        oram.write(key, str(key))
    for key in range(0, 7) :
        assert (oram.read(key) == str(key))

TestBasic()
