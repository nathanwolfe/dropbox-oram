class PosMap :
	
	def __init__(self):
		self._pos_map = {}

	def lookup(self, key) :
		if not key in self._pos_map :
			return -1
		return self._pos_map[key]

	def insert(self, key, value) :
		self._pos_map[key] = value
