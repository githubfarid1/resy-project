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
from settings import PYTHON_EXE
from tktimepicker import SpinTimePickerOld

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
		# pullButton.grid(row = 2, column = 2, sticky = (W), padx=20, pady=10)
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
		reservationlistButton = FrameButton(self, window, text="Add Reservation Type", class_frame=AddReservationFrame)
		periodlistButton = FrameButton(self, window, text="Add Period", class_frame=AddPeriodFrame)

		# extractButton = FrameButton(self, window, text="Extract PDF Diagram", class_frame=ExtractPdfFrame)
		# graburlButton = FrameButton(self, window, text="Grab URLs", class_frame=GrabUrlsFrame)
		# graburlVendorButton = FrameButton(self, window, text="Grab URLs By Vendor", class_frame=GrabUrlsVendorFrame)
		# pdfDownloadButton = FrameButton(self, window, text="Download PDF Diagram by File input", class_frame=MessickPdfDownload3Frame)

		# graburlVendor2Button = FrameButton(self, window, text="Grab URLs By Vendor ver.2", class_frame=GrabUrlsVendor2Frame)
		# pdfDownload2Button = FrameButton(self, window, text="Download PDF Diagram by File input ver.2", class_frame=MessickPdfDownload4Frame)

		# # # layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotv1Button.grid(column = 0, row = 1, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		reservationlistButton.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		periodlistButton.grid(column = 0, row = 3, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)

		# extractButton.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlButton.grid(column = 0, row = 3, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlVendorButton.grid(column = 0, row = 4, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# pdfDownloadButton.grid(column = 0, row = 5, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# graburlVendor2Button.grid(column = 0, row = 6, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# pdfDownload2Button.grid(column = 0, row = 7, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)

class AddReservationFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		file = open("reservationlist.json", "r")
		listvalue = json.load(file)
		tmplist = [value for value in listvalue]
		setlist = set(tmplist)
		RESERVATION_LIST = sorted(list(setlist), key=str.casefold)

		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		titleLabel = TitleLabel(self, text="Add Reservation Type")
		valuentry = Entry(self, width=80)
		dlist = StringVar(value=RESERVATION_LIST)
		self.valueslist = Listbox(self, width=80, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(entry=valuentry, list=self.valueslist))
		saveButton = ttk.Button(self, text='Save', command = lambda:self.savelist(list=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		valuentry.grid(column = 0, row = 1, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		self.valueslist.grid(column = 0, row = 2, sticky=(W))
		saveButton.grid(column = 0, row = 3, sticky = (W,N))
		closeButton.grid(column = 0, row = 8, sticky = (E))
	def removeValue(self, event):
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
				messagebox.showinfo("Message box", f"`{self.valueslist.get(i)}` deleted..")
		self.valueslist.delete(selection)
		

	def savelist(self, **kwargs):
		with open("reservationlist.json", "w") as final:
			json.dump(kwargs['list'].get(0, END), final)
		messagebox.showinfo("Message box","Reservation List saved..")

	def addlist(self, **kwargs):
		kwargs['list'].insert(0, kwargs['entry'].get())
		kwargs['entry'].delete(0, END)
		messagebox.showinfo("Message box","New Reservation added..")

class AddPeriodFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		file = open("periodlist.json", "r")
		listvalue = json.load(file)
		tmplist = [value for value in listvalue]
		setlist = set(tmplist)
		PERIOD_LIST = sorted(list(setlist), key=str.casefold)

		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		titleLabel = TitleLabel(self, text="Add Period")
		valuentry = Entry(self, width=80)
		dlist = StringVar(value=PERIOD_LIST)
		self.valueslist = Listbox(self, width=80, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(entry=valuentry, list=self.valueslist))
		saveButton = ttk.Button(self, text='Save', command = lambda:self.savelist(list=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		valuentry.grid(column = 0, row = 1, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		self.valueslist.grid(column = 0, row = 2, sticky=(W))
		saveButton.grid(column = 0, row = 3, sticky = (W,N))
		closeButton.grid(column = 0, row = 8, sticky = (E))
	def removeValue(self, event):
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
				messagebox.showinfo("Message box", f"`{self.valueslist.get(i)}` deleted..")
		self.valueslist.delete(selection)
		

	def savelist(self, **kwargs):
		with open("periodlist.json", "w") as final:
			json.dump(kwargs['list'].get(0, END), final)
		messagebox.showinfo("Message box","Period List saved..")

	def addlist(self, **kwargs):
		kwargs['list'].insert(0, kwargs['entry'].get())
		kwargs['entry'].delete(0, END)
		messagebox.showinfo("Message box","New Period added..")

class ResyBotv1Frame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		file = open("reservationlist.json", "r")
		listvalue = json.load(file)
		tmplist = [value for value in listvalue]
		setlist = set(tmplist)
		RESERVATION_LIST = sorted(list(setlist), key=str.casefold)

		file = open("periodlist.json", "r")
		listvalue = json.load(file)
		tmplist = [value for value in listvalue]
		setlist = set(tmplist)
		PERIOD_LIST = sorted(list(setlist), key=str.casefold)

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
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)


		
		# populate
		titleLabel = TitleLabel(self, text="Resy Bot v1")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Date: ")
		timelabel = Label(self, text="Time: ")
		seatslabel = Label(self, text="Seats: ")
		periodlabel = Label(self, text="Period: ")
		reservationlabel = Label(self, text="Reservation Type: ")
		urlentry = Entry(self, width=80)
		urlentry.insert(0, "https://resy.com/cities/new-york-ny/venues/zensushi-omakase")
		dateentry = DateEntry(self, width= 20, date_pattern='mm/dd/yyyy')
		timeentry = SpinTimePickerOld(self)
		timeentry.addHours12()
		timeentry.addMinutes()
		timeentry.addPeriod()
		defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=50, textvariable=defseat, state="readonly")
		seatsentry.insert(0,2)
		periodentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly")
		periodentry['values'] = [period for period in PERIOD_LIST]
		periodentry.current(0)
		reservationentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=30)
		reservationentry['values'] = [reservation for reservation in RESERVATION_LIST]
		reservationentry.current(0)
		closeButton = CloseButton(self)
		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(url=urlentry, date=dateentry, time=timeentry, seats=seatsentry, period=periodentry, reservation=reservationentry))
		
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		urllabel.grid(column = 0, row = 1, sticky=(W))
		urlentry.grid(column = 0, row = 1, sticky=(E))
		datelabel.grid(column = 0, row = 2, sticky=(W))
		dateentry.grid(column = 0, row = 2, sticky=(E))
		timelabel.grid(column = 0, row = 3, sticky=(W))
		timeentry.grid(column = 0, row = 3, sticky=(E))
		seatslabel.grid(column = 0, row = 4, sticky=(W))
		seatsentry.grid(column = 0, row = 4, sticky=(E))
		periodlabel.grid(column = 0, row = 5, sticky=(W))
		periodentry.grid(column = 0, row = 5, sticky=(E))
		reservationlabel.grid(column = 0, row = 6, sticky=(W))
		reservationentry.grid(column = 0, row = 6, sticky=(E))

		runButton.grid(column = 0, row = 7, sticky = (E))
		closeButton.grid(column = 0, row = 8, sticky = (E))

	def run_process(self, **kwargs):
		hour = str(kwargs['time'].hours())
		period = kwargs['time'].period().replace(".","").upper()
		if len(str(kwargs['time'].minutes())) == 1:
			minute = f"0{str(kwargs['time'].minutes())}"
		else:
			minute = str(kwargs['time'].minutes())
		formatted_time = f"{hour}:{minute} {period}"
		run_module(comlist=[PYLOC, "modules/resybotv1.py", "-u", '{}'.format(kwargs['url'].get()), "-d", '{}'.format(kwargs['date'].get_date()), "-t", '{}'.format(formatted_time), "-s", '{}'.format(kwargs['seats'].get()), "-p", '{}'.format(kwargs['period'].get()), "-r", '{}'.format(kwargs['reservation'].get()) ])

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
		PYLOC = PYTHON_EXE

main()