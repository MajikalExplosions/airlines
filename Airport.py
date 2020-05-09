class Airport:
	def __init(self,code, city, timezone): 
		self.code = code
		self.city = city
		self.timezone = timezone

	def getCode(self):
		return self.code

	def getCity(self):
		return self.city

	def getTimezone(self):
		return self.timezone
