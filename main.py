from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from pathlib import Path
import os
import git
import sys
from sys import platform
from subprocess import Popen, check_call
import warnings
import shutil
from settings import PYTHON_EXE, CHROME_USER_DATA
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

def savejson(filename, valuelist, value=False):
	# breakpoint()
	if value:
		file = open(filename, "r")
		tmplist = json.load(file)
		found = False
		# breakpoint()
		for lst1 in tmplist:
			if lst1['profilename'] == value:
				messagebox.showerror("Message box","profile name found")
				found = True
				break
		# breakpoint()
		if not found:
			with open(filename, "w") as final:
				json.dump(valuelist, final)
			return True
		else:
			return False
	else:
		# breakpoint()
		with open(filename, "w") as final:
			try:
				json.dump(valuelist.get(0, END), final)
			except:
				json.dump(valuelist, final)
		return True


class Window(Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title('Resy.com Bot Application @2024')
		# self.resizable(0, 0)
		self.gitme = git.cmd.Git(os.getcwd())
		self.gitme.fetch()
		# breakpoint()
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
		pullButton = Button(self, text='Update Script', command=lambda:self.gitPull())
		# settingButton = ttk.Button(self, text='Chrome Setup', command=lambda:chromeSetup())
		
		exitButton.grid(row=2, column=3, sticky=(E), padx=20, pady=5)
		pullButton.grid(row=2, column=0, sticky = (W), padx=20, pady=5)
		if not "up to date" in self.gitme.status():
			pullButton['state'] = "normal"
			pullButton['bg'] = "red"
		else:
			pullButton['state'] = "disabled"

		mainFrame = MainFrame(self)
		mainFrame.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)

	def gitPull(self):
		self.gitme.pull()
		run_module(comlist=[PIPLOC, "-r", "requirements.txt"])
		messagebox.showinfo(title='Info', message='the scripts has updated, reopen the application...')
		sys.exit()

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
		resybotv2Button = FrameButton(self, window, text="Resy Bot v2", class_frame=ResyBotv2Frame)
		resybotv3Button = FrameButton(self, window, text="Resy Bot v3", class_frame=ResyBotv3Frame)
		listbookButton = FrameButton(self, window, text="List of Bookings", class_frame=ListCommandFrame)

		reservationlistButton = FrameButton(self, window, text="Update Reservation Type", class_frame=AddReservationFrame)
		periodlistButton = FrameButton(self, window, text="Update Period", class_frame=AddPeriodFrame)
		chromiumProfileButton = FrameButton(self, window, text="Update Chromium Profile", class_frame=ChromiumProfileFrame)
		# setupChromiumButton = FrameButton(self, window, text="Chromium Profile Tester", class_frame=SetupChromiumFrame)
		UpdateTokenButton = FrameButton(self, window, text="Update Profile Token", class_frame=UpdateTokenFrame)


		# # # layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotv2Button.grid(column = 0, row = 1, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotv3Button.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		listbookButton.grid(column = 0, row = 3, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		reservationlistButton.grid(column = 0, row = 4, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		periodlistButton.grid(column = 0, row = 5, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		chromiumProfileButton.grid(column = 0, row = 6, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		# setupChromiumButton.grid(column = 0, row = 7, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		UpdateTokenButton.grid(column = 0, row = 7, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)

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
		titleLabel = TitleLabel(self, text="Update Reservation Type")
		valuentry = Entry(self, width=80)
		dlist = StringVar(value=RESERVATION_LIST)
		self.valueslist = Listbox(self, width=80, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(entry=valuentry, valuelist=self.valueslist))
		saveButton = ttk.Button(self, text='Save', command = lambda:self.savelist(valuelist=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		valuentry.grid(column = 0, row = 1, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		self.valueslist.grid(column = 0, row = 2, sticky=(W))
		# saveButton.grid(column = 0, row = 3, sticky = (W,N))
		closeButton.grid(column = 0, row = 8, sticky = (E))
	def removeValue(self, event):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
			messagebox.showinfo("Message box", f"`{self.valueslist.get(i)}` deleted..")
		self.valueslist.delete(selection)
		savejson(filename="reservationlist.json", valuelist=self.valueslist)

	def savelist(self, **kwargs):
		with open("reservationlist.json", "w") as final:
			json.dump(kwargs['valuelist'].get(0, END), final)
		messagebox.showinfo("Message box","Reservation List saved..")

	def addlist(self, **kwargs):
		kwargs['valuelist'].insert(0, kwargs['entry'].get())
		kwargs['entry'].delete(0, END)
		savejson(filename="reservationlist.json", valuelist=kwargs['valuelist'])
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
		titleLabel = TitleLabel(self, text="Update Period")
		valuentry = Entry(self, width=80)
		dlist = StringVar(value=PERIOD_LIST)
		self.valueslist = Listbox(self, width=80, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(entry=valuentry, valuelist=self.valueslist))
		saveButton = ttk.Button(self, text='Save', command = lambda:self.savelist(valuelist=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		valuentry.grid(column = 0, row = 1, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		self.valueslist.grid(column = 0, row = 2, sticky=(W))
		# saveButton.grid(column = 0, row = 3, sticky = (W,N))
		closeButton.grid(column = 0, row = 8, sticky = (E))
	
	def removeValue(self, event):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
			messagebox.showinfo("Message box", f"`{self.valueslist.get(i)}` deleted..")
		self.valueslist.delete(selection)
		savejson(filename="periodlist.json", valuelist=self.valueslist)	

	def savelist(self, **kwargs):
		with open("periodlist.json", "w") as final:
			json.dump(kwargs['valuelist'].get(0, END), final)
		messagebox.showinfo("Message box","Period List saved..")

	def addlist(self, **kwargs):
		kwargs['valuelist'].insert(0, kwargs['entry'].get())
		kwargs['entry'].delete(0, END)
		savejson(filename="periodlist.json", valuelist=kwargs['valuelist'])
		messagebox.showinfo("Message box","New Period added..")

class ChromiumProfileFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		file = open("profilelist.json", "r")
		self.profilelist = json.load(file)
		PROFILE_LIST = [f"{value['profilename']} | {value['email']} | {value['password']}" for value in self.profilelist]
		# setlist = set(tmplist)
		# PROFILE_LIST = sorted(self.profilelist, key=str.casefold)
		# breakpoint()
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
		titleLabel = TitleLabel(self, text="Update Chromium Profile")
		profilenamentry = EntryWithPlaceholder(self, width=80, placeholder="Profile Name (No Space allowed)")
		emailentry = EntryWithPlaceholder(self, width=80, placeholder="Email")
		passwordentry = EntryWithPlaceholder(self, width=80, placeholder="Password")

		dlist = StringVar(value=PROFILE_LIST)
		self.valueslist = Listbox(self, width=80, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(profilename=profilenamentry, email=emailentry, password=passwordentry, valuelist=self.valueslist))
		saveButton = ttk.Button(self, text='Save', command = lambda:self.savelist(valuelist=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		profilenamentry.grid(column = 0, row = 1, sticky=(W))
		emailentry.grid(column = 0, row = 2, sticky=(W))
		passwordentry.grid(column = 0, row = 3, sticky=(W))
		self.valueslist.grid(column = 0, row = 4, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		# saveButton.grid(column = 0, row = 3, sticky = (W,N))
		closeButton.grid(column = 0, row = 8, sticky = (E))
	
	def removeValue(self, event):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
			strselect = self.valueslist.get(i).split(" | ")[0]
			messagebox.showinfo("Message box", f"`{strselect}` deleted..")
		self.valueslist.delete(selection)
		tmplist = []
		for dl in self.profilelist:
			if dl['profilename'] != strselect:
				tmplist.append(dl)
		self.profilelist = tmplist.copy()
		savejson(filename="profilelist.json", valuelist=self.profilelist)
		try:	
			shutil.rmtree(CHROME_USER_DATA + os.path.sep + strselect)
		except:
			pass
	def addlist(self, **kwargs):
		self.profilelist.append({"profilename": kwargs['profilename'].get(), "email": kwargs['email'].get(), "password": kwargs['password'].get()})
		if savejson(filename="profilelist.json", valuelist=self.profilelist, value=kwargs['profilename'].get()):
			kwargs['valuelist'].insert(0, f"{kwargs['profilename'].get()} | {kwargs['email'].get()} | {kwargs['password'].get()}")
		else:
			# breakpoint()
			self.profilelist.pop()
		
		kwargs['profilename'].delete(0, END)
		kwargs['email'].delete(0, END)
		kwargs['password'].delete(0, END)
		
		# messagebox.showinfo("Message box","New Period added..")

class SetupChromiumFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')

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
				
		titleLabel = TitleLabel(self, 'Chromium Profiles')
		closeButton = CloseButton(self)
		file = open("profilelist.json", "r")
		profilelisttmp = json.load(file)
		profileList = []
		for text in [value['profilename'] for value in profilelisttmp]:
			profileList.append(ttk.Button(self, text=text, command=lambda pro=text:self.chromeTester(pro)))

		# layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=4)
		closeButton.grid(column = 0, row = 6, sticky = (E, N, S), columnspan=4)

		colnum = 0
		rownum = 1
		for profile in profileList:
			if colnum == 3:
				colnum = 0
				rownum += 1
			profile.grid(column = colnum, row = rownum, sticky=(W, E, N, S), padx=15, pady=5)
			colnum += 1

	def chromeTester(self, profile):
		file = open("profilelist.json", "r")
		profilelisttmp = json.load(file)
		profileselected = [value for value in profilelisttmp if value['profilename']==profile]
		run_module(comlist=[PYLOC, "modules/chromium_setup.py", "-cp", profile, "-em", profileselected[0]['email'], "-pw", profileselected[0]['password'] ])

class UpdateTokenFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')

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
				
		titleLabel = TitleLabel(self, 'Update Token Profile')
		closeButton = CloseButton(self)
		file = open("profilelist.json", "r")
		profilelisttmp = json.load(file)
		profileList = []
		for text in [value['profilename'] for value in profilelisttmp]:
			profileList.append(ttk.Button(self, text=text, command=lambda pro=text:self.chromeTester(pro)))

		# layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=4)
		closeButton.grid(column = 0, row = 6, sticky = (E, N, S), columnspan=4)

		colnum = 0
		rownum = 1
		for profile in profileList:
			if colnum == 3:
				colnum = 0
				rownum += 1
			profile.grid(column = colnum, row = rownum, sticky=(W, E, N, S), padx=15, pady=5)
			colnum += 1

	def chromeTester(self, profile):
		file = open("profilelist.json", "r")
		profilelisttmp = json.load(file)
		profileselected = [value for value in profilelisttmp if value['profilename']==profile]
		run_module(comlist=[PYLOC, "modules/update_token.py", "-cp", profile, "-em", profileselected[0]['email'], "-pw", profileselected[0]['password'] ])

class ListCommandFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		file = open("commandlist.json", "r")
		self.commandlist = json.load(file)
		commandlist = ["{} | {} | {} | {} | {} | {}".format(str(value['baseurl']).split("/")[-1], value['date'], value['time'], value['seats'], value['period'], value['reservation_type'] )  for value in self.commandlist]
		file = open("profilelist.json", "r")
		self.profilelist = json.load(file)
		PROFILE_LIST = [f"{value['profilename']} | {value['email']} | {value['password']}" for value in self.profilelist]

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
		titleLabel = TitleLabel(self, text="List Bot's Command")

		dlist = StringVar(value=commandlist)
		self.valueslist = Listbox(self, width=120, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		chprofilelabel = Label(self, text="Chromium Profile: ")
		headlesslabel = Label(self, text="Headless Mode: ")
		proclabel = Label(self, text="Execute Mode: ")
		nstoplabel = Label(self, text="Nonstop Checking: ")
		closeButton = CloseButton(self)
		chprofileentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=30)
		chprofileentry['values'] = [profile for profile in PROFILE_LIST]
		chprofileentry.current(0)
		headlessentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=5)
		headlessentry['values'] = ['No','Yes']
		headlessentry.current(0)
		procentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=10)
		procentry['values'] = ['Single','Multiple']
		procentry.current(0)
		nstopentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=5)
		nstopentry['values'] = ['No','Yes']
		nstopentry.current(0)

		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(profile=chprofileentry, headless=headlessentry, exemode=procentry, nstop=nstopentry))

		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		self.valueslist.grid(column = 0, row = 1, sticky=(W))
		chprofilelabel.grid(column = 0, row = 2, sticky=(W))
		chprofileentry.grid(column = 0, row = 2, sticky=(E))
		headlesslabel.grid(column = 0, row = 3, sticky=(W))
		headlessentry.grid(column = 0, row = 3, sticky=(E))
		proclabel.grid(column = 0, row = 4, sticky=(W))
		procentry.grid(column = 0, row = 4, sticky=(E))
		nstoplabel.grid(column = 0, row = 5, sticky=(W))
		nstopentry.grid(column = 0, row = 5, sticky=(E))

		runButton.grid(column = 0, row = 6, sticky = (E))
		closeButton.grid(column = 0, row = 7, sticky = (E))
	
	def removeValue(self, event):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
			strselect = self.valueslist.get(i)
			messagebox.showinfo("Message box", f"`{strselect}` deleted..")
		self.valueslist.delete(selection)
		tmplist = []
		for dl in self.commandlist:
			if "{} | {} | {} | {} | {} | {}".format(str(dl['baseurl']).split("/")[-1], dl['date'], dl['time'], dl['seats'], dl['period'], dl['reservation_type']) != strselect:
				tmplist.append(dl)
		self.commandlist = []
		self.commandlist = tmplist.copy()
		savejson(filename="commandlist.json", valuelist=self.commandlist)

	def run_process(self, **kwargs):
		profile = kwargs['profile'].get().split("|")[0].strip()
		email = kwargs['profile'].get().split("|")[1].strip()
		password = kwargs['profile'].get().split("|")[2].strip()
		if kwargs['exemode'].get() == 'Single':
			run_module(comlist=[PYLOC, "modules/resybotv3.py", "-cp", profile, "-em", email, "-pw", password, "-hl", '{}'.format(kwargs['headless'].get())])
		else:
			for command in self.commandlist:
				run_module(comlist=[PYLOC, "modules/resybotv3b.py", "-u", '{}'.format(command['baseurl']), "-d", '{}'.format(command['date']), "-t", '{}'.format(command['time']), "-s", '{}'.format(command['seats']), "-p", '{}'.format(command['period']), "-r", '{}'.format(command['reservation_type']), "-cp", profile, "-em", email, "-pw", password, "-hl", '{}'.format(kwargs['headless'].get()), "-ns", '{}'.format(kwargs['nstop'].get())])
				
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
		self.rowconfigure(9, weight=1)
		
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
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=defseat, state="readonly", width=5)
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
		# breakpoint()
		run_module(comlist=[PYLOC, "modules/resybotv1.py", "-u", '{}'.format(kwargs['url'].get()), "-d", '{}'.format(kwargs['date'].get_date()), "-t", '{}'.format(formatted_time), "-s", '{}'.format(kwargs['seats'].get()), "-p", '{}'.format(kwargs['period'].get()), "-r", '{}'.format(kwargs['reservation'].get())])

class ResyBotv2Frame(ttk.Frame):
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

		file = open("profilelist.json", "r")
		self.profilelist = json.load(file)
		PROFILE_LIST = [f"{value['profilename']} | {value['email']} | {value['password']}" for value in self.profilelist]

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
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
		self.rowconfigure(11, weight=1)
		
		# populate
		titleLabel = TitleLabel(self, text="Resy Bot v2")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Date: ")
		timelabel = Label(self, text="Time: ")
		seatslabel = Label(self, text="Seats: ")
		periodlabel = Label(self, text="Period: ")
		reservationlabel = Label(self, text="Reservation Type: ")
		chprofilelabel = Label(self, text="Chromium Profile: ")
		headlesslabel = Label(self, text="Headless Mode: ")


		urlentry = Entry(self, width=80)
		urlentry.insert(0, "https://resy.com/cities/new-york-ny/venues/zensushi-omakase")
		dateentry = DateEntry(self, width= 20, date_pattern='mm/dd/yyyy')
		timeentry = SpinTimePickerOld(self)
		timeentry.addHours12()
		timeentry.addMinutes()
		timeentry.addPeriod()
		defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=defseat, state="readonly", width=5)
		seatsentry.insert(0,2)
		periodentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly")
		periodentry['values'] = [period for period in PERIOD_LIST]
		periodentry.current(0)
		reservationentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=30)
		reservationentry['values'] = [reservation for reservation in RESERVATION_LIST]
		reservationentry.current(0)
		chprofileentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=30)
		chprofileentry['values'] = [profile for profile in PROFILE_LIST]
		chprofileentry.current(0)
		headlessentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=5)
		headlessentry['values'] = ['No','Yes']
		headlessentry.current(0)

		closeButton = CloseButton(self)
		runButton = ttk.Button(self, text='Run Process', command = lambda:self.run_process(url=urlentry, date=dateentry, time=timeentry, seats=seatsentry, period=periodentry, reservation=reservationentry, profile=chprofileentry, headless=headlessentry))
		
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
		chprofilelabel.grid(column = 0, row = 7, sticky=(W))
		chprofileentry.grid(column = 0, row = 7, sticky=(E))
		headlesslabel.grid(column = 0, row = 8, sticky=(W))
		headlessentry.grid(column = 0, row = 8, sticky=(E))

		runButton.grid(column = 0, row = 9, sticky = (E))
		closeButton.grid(column = 0, row = 10, sticky = (E))

	def run_process(self, **kwargs):
		hour = str(kwargs['time'].hours())
		period = kwargs['time'].period().replace(".","").upper()
		if len(str(kwargs['time'].minutes())) == 1:
			minute = f"0{str(kwargs['time'].minutes())}"
		else:
			minute = str(kwargs['time'].minutes())
		formatted_time = f"{hour}:{minute} {period}"
		# breakpoint()
		profile = kwargs['profile'].get().split("|")[0].strip()
		email = kwargs['profile'].get().split("|")[1].strip()
		password = kwargs['profile'].get().split("|")[2].strip()
		run_module(comlist=[PYLOC, "modules/resybotv2.py", "-u", '{}'.format(kwargs['url'].get()), "-d", '{}'.format(kwargs['date'].get_date()), "-t", '{}'.format(formatted_time), "-s", '{}'.format(kwargs['seats'].get()), "-p", '{}'.format(kwargs['period'].get()), "-r", '{}'.format(kwargs['reservation'].get()), "-cp", profile, "-em", email, "-pw", password, "-hl", '{}'.format(kwargs['headless'].get() ) ])

class ResyBotv3Frame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		file = open("commandlist.json", "r")
		self.commandlist = json.load(file)

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

		file = open("profilelist.json", "r")
		self.profilelist = json.load(file)
		PROFILE_LIST = [f"{value['profilename']} | {value['email']} | {value['password']}" for value in self.profilelist]

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
		self.rowconfigure(9, weight=1)
		
		# populate
		titleLabel = TitleLabel(self, text="Resy Bot v3")
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
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=defseat, state="readonly", width=5)
		seatsentry.insert(0,2)
		periodentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly")
		periodentry['values'] = [period for period in PERIOD_LIST]
		periodentry.current(0)
		reservationentry = ttk.Combobox(self, textvariable=StringVar(), state="readonly", width=30)
		reservationentry['values'] = [reservation for reservation in RESERVATION_LIST]
		reservationentry.current(0)

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Save Booking', command = lambda:self.savelist(url=urlentry, date=dateentry, time=timeentry, seats=seatsentry, period=periodentry, reservation=reservationentry))
		# listButton = ttk.Button(self, text='List Commands', command = lambda:self.savelist(url=urlentry, date=dateentry, time=timeentry, seats=seatsentry, period=periodentry, reservation=reservationentry))
		listButton = FrameButton(self, window, text="List Bookings", class_frame=ListCommandFrame)
		
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

		saveButton.grid(column = 0, row = 7, sticky = (E))
		# listButton.grid(column = 0, row = 7, sticky = (W))
		closeButton.grid(column = 0, row = 8, sticky = (E))

	def savelist(self, **kwargs):
		hour = str(kwargs['time'].hours())
		period = kwargs['time'].period().replace(".","").upper()
		if len(str(kwargs['time'].minutes())) == 1:
			minute = f"0{str(kwargs['time'].minutes())}"
		else:
			minute = str(kwargs['time'].minutes())
		formatted_time = f"{hour}:{minute} {period}"
		# breakpoint()
		self.commandlist.append({"baseurl":kwargs['url'].get(), "date": str(kwargs['date'].get_date()), "time": formatted_time, "seats":kwargs['seats'].get(), "period":kwargs['period'].get(), "reservation_type":kwargs['reservation'].get()})
		savejson(filename="commandlist.json", valuelist=self.commandlist)
		messagebox.showinfo("Message box","Booking list Saved")

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

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', width=30):
        super().__init__(master, width=width)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        # self.width = width
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

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
		PIPLOC = "pip"
	elif platform == "win32":
		PYLOC = PYTHON_EXE
		PIPLOC = os.getcwd() + os.sep + r"venv\Scripts\pip.exe"

main()
