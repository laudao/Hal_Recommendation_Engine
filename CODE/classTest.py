class Test:
	def __init__(self, attr1=None, attr2=None):
		self.attr1 = attr1
		self.attr2 = attr2

	@property
	def attr1(self):
		return self.__attr1

	@property
	def attr2(self):
		return self.__attr2

	@attr1.setter
	def attr1(self, x):
		self.__attr1 = x

	@attr2.setter
	def attr2(self, x):
		self.__attr2 = self.attr1 + 1

t = Test(2)
print(t.attr2)
