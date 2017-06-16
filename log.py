import tkinter as tk


class Log(object):
	__levels = {}
	text = None

	@classmethod
	def level(cls, level, value):
		cls.__levels[level] = value

	@classmethod
	def message(cls, level, message):
		if level in cls.__levels and cls.__levels[level]:
			if cls.text:
				cls.text.insert(tk.END, "{0}\n".format(str(message)))
			else:
				print(str(message))
