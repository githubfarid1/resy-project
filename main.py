from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import filedialog
from tkinter import messagebox
import tkinter
from tkcalendar import Calendar, DateEntry
from pathlib import Path
import os
import sys
from sys import platform
from subprocess import Popen, check_call
import git
import warnings
import shutil
import settings as s

warnings.filterwarnings("ignore", category=UserWarning)
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
import json


warnings.filterwarnings("ignore", category=UserWarning)
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
import json

# def chromeSetup():
#     if platform == "linux" or platform == "linux2":
#         CHROME = "google-chrome"
#     elif platform == "win32":
#         CHROME = s.CHROME_EXE
#     Popen([CHROME, "chrome://settings/","--user-data-dir={}".format(s.CHROME_USER_DATA), "--profile-directory={}".format(s.CHROME_PROFILE)])

class Window(Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title('Resy Bot Application')
		# self.resizable(0, 0)
		self.grid_propagate(False)
		width = 700
		height = 650
		swidth = self.winfo_screenwidth()
		sheight = self.winfo_screenheight()
		newx = int((swidth/2) - (width/2))
		newy = int((sheight/2) - (height/2))
		self.geometry(f"{width}x{height}+{newx}+{newy}")
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)

		self.rowconfigure(0, weight=1)
		exitButton = ttk.Button(self, text="Exit", command=lambda:self.procexit())
		pullButton = ttk.Button(self, text='Update Script', command=lambda:self.gitPull())
		# settingButton = ttk.Button(self, text='Chrome Setup', command=lambda:chromeSetup())
		
		exitButton.grid(row=2, column=3, sticky=(E), padx=20, pady=5)
		pullButton.grid(row = 2, column = 2, sticky = (W), padx=20, pady=10)
		# settingButton.grid(row = 2, column = 0, sticky = (W), padx=20, pady=10)

		mainFrame = MainFrame(self)
		mainFrame.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)

	def gitPull(self):
		git_dir = os.getcwd() 
		g = git.cmd.Git(git_dir)
		g.pull()		
		messagebox.showinfo(title='Info', message='the scripts has updated..')


	def procexit(self):
		try:
			for p in Path(".").glob("__tmp*"):
				p.unlink()
		except:
			pass
		sys.exit()

class MainFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		# self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=2)
		framestyle = ttk.Style()
		framestyle.configure('TFrame', background='#C1C1CD')
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove', style='TFrame')
		
		# self.place(anchor=CENTER)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		# self.columnconfigure(3, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
  
		
		titleLabel = TitleLabel(self, 'Main Menu')
		resybotv1Button = FrameButton(self, window, text="Resy Bot v1", class_frame=ResyBotv1Frame)
		# extractButton = FrameButton(self, window, text="Extract PDF Diagram", class_frame=ExtractPdfFrame)
		# graburlButton = FrameButton(self, window, text="Grab URLs", class_frame=GrabUrlsFrame)
		# graburlVendorButton = FrameButton(self, window, text="Grab URLs By Vendor", class_frame=GrabUrlsVendorFrame)
		# pdfDownloadButton = FrameButton(self, window, text="Download PDF Diagram by File input", class_frame=MessickPdfDownload3Frame)

		# graburlVendor2Button = FrameButton(self, window, text="Grab URLs By Vendor ver.2", class_frame=GrabUrlsVendor2Frame)
		# pdfDownload2Button = FrameButton(self, window, text="Download PDF Diagram by File input ver.2", class_frame=MessickPdfDownload4Frame)

		# # # layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotv1Button.grid(column = 0, row = 1, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# extractButton.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlButton.grid(column = 0, row = 3, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlVendorButton.grid(column = 0, row = 4, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# pdfDownloadButton.grid(column = 0, row = 5, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlVendor2Button.grid(column = 0, row = 6, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# pdfDownload2Button.grid(column = 0, row = 7, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
class ResyBotv1Frame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		
		# populate
		titleLabel = TitleLabel(self, text="Dowload Catalog Product from messicks.com")
		closeButton = CloseButton(self)

		labelsname = Label(self, text="Product URL:")
		# urltxt = Entry(self, width=65)
		urltxt = Text(self, height=12, width=40) 
		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(urltxt=urltxt.get("1.0", END) ))
		
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		labelsname.grid(column = 0, row = 3, sticky=(W))
		urltxt.grid(column = 0, row = 3, pady=10)
		runButton.grid(column = 0, row = 5, sticky = (E))
		closeButton.grid(column = 0, row = 6, sticky = (E, N, S))

	def run_process(self, **kwargs):
			# messagebox.showwarning(title='Warning', message='')
			urls = str(kwargs['urltxt']).replace("\n", "#")
			run_module(comlist=[PYLOC, "modules/catmessick.py", "-url", urls])

class FrameButton(ttk.Button):
	def __init__(self, parent, window, **kwargs):
		super().__init__(parent)
		# object attributes
		self.text = kwargs['text']
		# configure
		self.config(text = self.text, command = lambda : kwargs['class_frame'](window))

class TitleLabel(ttk.Label):
	def __init__(self, parent, text):
		super().__init__(parent)
		font_tuple = ("Comic Sans MS", 20, "bold")
		self.config(text=text, font=font_tuple, anchor="center")

class CloseButton(ttk.Button):
	def __init__(self, parent):
		super().__init__(parent)
		self.config(text = '< Back', command=lambda : parent.destroy())

def run_module(comlist):
	if platform == "linux" or platform == "linux2":
		comlist[:0] = ["--"]
		comlist[:0] = ["gnome-terminal"]
		# print(comlist)
		Popen(comlist)
	elif platform == "win32":
		Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
	
	comall = ''
	for com in comlist:
		comall += com + " "
	print(comall)

def main():
	window = Window()
	window.mainloop()

if __name__ == "__main__":
	if platform == "linux" or platform == "linux2":
		PYLOC = "python"
	elif platform == "win32":
		PYLOC = s.PYTHON_EXE

main()