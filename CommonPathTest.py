import Util

f = open("CommonPathResult.txt")
results = f.read().splitlines()
f.close()
results = [res.split(' ') for res in results]

for res in results:
	leaf0, leaf1, maxCommonLevel = int(res[0]), int(res[1]), int(res[2])  	
			# format: [leaf0, leaf1, maxCommonLevel] Leaf is labeled with bucket ID. Root bucket is Bucket 0, Level 0.
			# My root bucket is Bucket 0; If yours is Bucket 1, increment leaf0 and leaf1 

	yourMaxCommonLevel = Util.getMaxLevel(leaf0+1, leaf1+1); # Your implementation
	
	if yourMaxCommonLevel != maxCommonLevel:
		print("results differ on \t {0} ^ {1}: {2} vs. {3}".format(leaf0, leaf1, yourMaxCommonLevel, maxCommonLevel))

# checked with the test! Algorithm works
