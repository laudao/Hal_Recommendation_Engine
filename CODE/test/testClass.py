class Test:
	def __init__(self, attr1, attr2):
		self.attr1 = attr1
		self.attr2 = attr2
		self.attr3 = '#'

	@property
	def attr1(self):
		return self.__attr1

	@property
	def attr2(self):
		return self.__attr2

	@property
	def attr3(self):
		return self.__attr3

	@attr1.setter
	def attr1(self, x):
		self.__attr1 = x
		try:
			self.attr3 = '*'
		except AttributeError:
			pass
	
	@attr2.setter
	def attr2(self, x):
		self.__attr2 = x
	
	@attr3.setter
	def attr3(self, x):
		if x == '#':
			self.__attr3 = "toto"
		elif x == '*':
			pass

t = Test(1, 3)
print(t.attr3)
