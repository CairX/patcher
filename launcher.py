import tkinter as tk


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.pack(fill=tk.BOTH, expand=True)

		self.log = tk.Text(self)
		self.log.pack(fill=tk.BOTH, expand=True)

		self.button = tk.Button(self, text="Update", command=self.say)
		self.button.pack()

	def say(self):
		self.log.insert(tk.END, "Button pressed.\n")


if __name__ == "__main__":
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
