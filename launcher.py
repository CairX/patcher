import downloader
import tkinter as tk

from configparser import ConfigParser


class Application(tk.Frame):
	def __init__(self, config, master=None):
		super().__init__(master)
		self.pack(fill=tk.BOTH, expand=True)

		self.config = config

		self.server_version = None
		self.local_version = None

		self.log = tk.Text(self)
		self.log.pack(fill=tk.BOTH, expand=True)
		self.counter = 0

		self.button = tk.Button(self)
		self.button.pack()
		self.compare_versions()

	def compare_versions(self):
		self.server_version = downloader.get_server_version(self.config["server"]["info"])
		self.local_version = downloader.get_local_version(self.config["local"]["install"])

		if self.local_version == self.server_version:
			self.button.config(text="Play", command=self.say)
		else:
			self.button.config(text="Update", command=self.install)

	def install(self):
		downloader.install(self.config["local"]["install"], self.config["server"]["versions"], self.server_version)
		self.compare_versions()

	def say(self):
		self.counter += 1
		self.log.insert(tk.END, "Button pressed " + str(self.counter) + " times.\n")


if __name__ == "__main__":
	downloader.Log.level("INFO", True)
	downloader.Log.level("WARNING", True)
	downloader.Log.level("ERROR", True)

	config = ConfigParser()
	config.read("downloader.ini")

	root = tk.Tk()
	app = Application(config, master=root)
	app.mainloop()
