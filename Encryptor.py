from Crypto.Cipher import AES
from Crypto.Util import strxor, Counter
from random import randint
import os

def mask(key, maskNum):
    cipher = AES.new(key, AES.MODE_ECB) 
    return cipher.encrypt(maskNum)

def decrypt(data, key):	# I modified this function to match the change in write(). Look at write() for explanation
    seed = int.from_bytes(data[0:16], byteorder="big")
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=seed))
    result = cipher.decrypt(data[16:])	  
    return result

def encrypt(data, key):
	# Your original code
	# + Good: clean and easy to follow.
	# - Drawback: you are truncating 'data' too many times. 
	#		If you think about it, you are constantly resizing an array, which we know is very inefficient
    '''	
    maskNum = randint(0, 1 << 128).to_bytes(16, byteorder="big")
    result = maskNum	
    maskBytes = mask(key, maskNum)
    while data != b"":
        currentSeg = data[:16]
        data = data[16:]
        currentMask = maskBytes[:len(currentSeg)]
        result += (int.from_bytes(currentSeg, byteorder="big") ^ int.from_bytes(currentMask, byteorder="big")).to_bytes(len(currentSeg), byteorder="big")
    '''		

    # My 1st round of optimization
    # 1) Do not truncate 'data'. Just take what you need each time.
	# 2) It turns out pycrypto provides a XOR function, strxor(), which is much more efficient than writing our own XOR
    # 3) I handle the left-over bits in the end so I don't have to check the length of currentSeg every time (this one is less important)
	# This version is about 2x faster than the original one.
    '''
    keylen = 16	
    numchunk = math.ceil(len(data) / keylen)	
    for i in range(0, numchunk):
        currentSeg = data[i*keylen:(i+1)*keylen]
        currentMask = maskBytes
        result += strxor.strxor(currentSeg, currentMask)
		
    currentSeg = data[numchunk*keylen:]
    currentMask = maskBytes[:len(currentSeg)]		
    result += strxor.strxor(currentSeg, currentMask)
    '''	
	
    # Now I will change maskNum to seed. Not a big deal, just a custom in crypto: we call the input 'seed', and the output 'mask'
    seed = randint(0, 1 << 128)	
    result = seed.to_bytes(16, byteorder="big")
	
    # My 2nd round of optimization
	# If you analyze the code of my 1st optimization, you will find that the bottleneck is strxor()
    # It is not strxor()'s fault; we call it too many times. 
    # In fact, strxor(x, y) can XOR x and y of arbitrary length, so we should batch our input for strxor().
	# Why? Because each function call has overhead, such as jump to the function, pass parameters, initialize local variables, return data ... 
    # In short, we want to reduce the number of function calls (but not at the cost of code readability. In this case, the code actually becomes simpler!)
    # This is about 1.5x faster than the last version
    '''	
    seeds = b""	
    for i in range(0, numchunk):	
        seeds += (seed+i).to_bytes(16, byteorder="big")	 # Why (seed+i).to_bytes? This requires advanced knowledge of crypto; you do not need to understand.
    maskBytes = mask(key, seeds)		
    result += strxor.strxor(maskBytes[:len(data)], data)
    '''

    # Now we call to_bytes() and += (yes, += is also a function) many times (in the 'for' loop), which is better than calling strxor(), but still not that great.
	# The 'for' loop can be replaced by a single line (either of the following two lines will do).
    # But the improvement is marginal (about 10%) and these are advanced Python syntax, so you don't have to know. 
    '''	
    # seeds = array.array('Q', range(seed, seed + numchunk)).tobytes()	# need to import array and use 64bit integer if using this one
    # seeds = b''.join([x.to_bytes(16, byteorder="big") for x in range(seed, seed + numchunk)])
    '''

    # The 3rd round of optimization requires more crypto experience. I also just found this out, so it is normal that you don't know	
    # The encryption we use is a standard one called AES counter (CTR) mode.
    # As a powerful and popular package, PyCrypto has implemented everything for us. So we do not need to manually handle chunk, XOR at all
    # We just need to specify CTR mode and pass in our seed (the interface of passing seed is a little weird and annoying)
    # Then just call cipher.encrypt() and we are done!
	# With this version, it is even hard to tell whether encryption is on or off! (PyCrypto did a great job!)
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=seed))
    result += cipher.encrypt(data)
    return result
