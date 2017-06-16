class Log(object):
	__levels = {}

	@classmethod
	def level(cls, level, value):
		cls.__levels[level] = value

	@classmethod
	def message(cls, level, message):
		if level in cls.__levels and cls.__levels[level]:
			print(message)
