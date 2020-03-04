class Zug:

	def __init__(self, data):
		self.data = data
		self.start = False
		self.ende = False

	def test(self):
		print("Yes" + str(self.start))

	def getAnkunft(self):
		if(self.start):
			return False
		else:
			#return self.data["departures"]["arrival"]
			ret = [""]
			da = self.data["departures"]
			for x in da:
				try:
					ret.append(x["arrival"])
				except Exception as e:
					pass
			return ret

	def getAbfahrt(self):
		if(self.ende == True):
			return False

	def printData(self):
		print(self.data)
