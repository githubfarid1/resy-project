from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from pathlib import Path
import os
import git
import sys
from sys import platform
from subprocess import Popen, check_call, PIPE, STDOUT
import warnings
import shutil
from settings import PYTHON_EXE, CHROME_USER_DATA
from tktimepicker import SpinTimePickerOld
from modules.database import Database
from datetime import datetime, timedelta

# db = Database("dbresy.db")
db = Database("db.sqlite3")

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

def convert24time(vtime):
	hour = str(vtime.hours())
	period = vtime.period().replace(".","").upper()
	if len(str(vtime.minutes())) == 1:
		minute = f"0{str(vtime.minutes())}"
	else:
		minute = str(vtime.minutes())
	return f"{hour}:{minute} {period}"

def convert24timeSecond(vtime):
	hour = str(vtime.hours())
	period = vtime.period().replace(".","").upper()
	if len(str(vtime.minutes())) == 1:
		minute = f"0{str(vtime.minutes())}"
	else:
		minute = str(vtime.minutes())
	if len(str(vtime.seconds())) == 1:
		second = f"0{str(vtime.seconds())}"
	else:
		second = str(vtime.seconds())

	return f"{hour}:{minute}:{second} {period}"

class Window(Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title('Resy.com Bot Application @2024')
		# self.resizable(0, 0)
		self.gitme = git.cmd.Git(os.getcwd())
		self.gitme.fetch()
		# breakpoint()
		self.grid_propagate(False)
		# width = 1330
		# height = 720
		# swidth = self.winfo_screenwidth()
		# sheight = self.winfo_screenheight()
		self.state("zoomed")
		# newx = int((swidth/2) - (width/2))
		# newy = int((sheight/2) - (height/2))
		# self.geometry(f"{width}x{height}+{newx}+{newy}")
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)

		self.rowconfigure(0, weight=1)
		exitButton = ttk.Button(self, text="Exit", command=lambda:self.procexit())
		pullButton = Button(self, text='Update Script', command=lambda:self.gitPull())
		updatedataButton = Button(self, text='Update Data', command=lambda:self.updateData())
		# settingButton = ttk.Button(self, text='Chrome Setup', command=lambda:chromeSetup())
		
		exitButton.grid(row=2, column=3, sticky=(E), padx=20, pady=5)
		updatedataButton.grid(row=2, column=1, sticky=(E), padx=20, pady=5)
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
		run_module(comlist=[PIPLOC, "install", "-r", "requirements.txt"])
		
		messagebox.showinfo(title='Info', message='the scripts has updated, reopen the application...')
		sys.exit()

	def procexit(self):
		try:
			for p in Path(".").glob("__tmp*"):
				p.unlink()
		except:
			pass
		sys.exit()

	def updateData(self):
		dbold = Database("dbresy.db")
		if len(db.viewReservation()) == 0:
			for rs in db.reservationValues():
				db.insertReservation(name=rs)

		if len(db.viewAccount()) == 0:
			for rs in db.profileValues2():
				db.insertAccount(email=rs['email'], password=rs['password'], token=rs['token'], payment_method_id=rs['payment_method_id'], api_key=rs['api_key'])
			db.insertAccount(email="<Not Set>", password="", token="", payment_method_id="", api_key="")

		if len(db.viewProxy()) == 0:
			for rs in db.proxyValues2():
				db.insertProxy(name=rs['profilename'], http=rs['http_proxy'], https=rs['https_proxy'])

		if len(db.viewCommand()) == 0:
			for dt in dbold.viewCommand():
				db.insertCommand(url=dt[18], datewanted=dt[2], timewanted=dt[3], hoursba=dt[4], seats=dt[5],reservation=dt[6],rundate=dt[7],runtime=dt[8], runnow=dt[9],account=dt[10], nonstop=dt[11], duration=dt[12],proxy=dt[13],retry=dt[14],minidle=dt[15],maxidle=dt[16])
		messagebox.showinfo(title='Info', message='the Data has updated...')

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
		resybotv4Button = FrameButton(self, window, text="Resy Bot Booking Form", class_frame=ResyBotv5Frame)
		resybotcheckButton = FrameButton(self, window, text="Resy Bot Checking Availability Form", class_frame=ResyBotCheckFrame)
		resybotbookingButton = FrameButton(self, window, text="Resy Bot Checking Availability and Booking Form", class_frame=ResyBotBookingFrame)
		# reservationlistButton = FrameButton(self, window, text="Update Reservation Type", class_frame=AddReservationFrame)
		reservationlistButton = FrameButton(self, window, text="Reservation Type Form", class_frame=RerservationFrame)

		# chromiumProfileButton = FrameButton(self, window, text="Update Chromium Profile", class_frame=ChromiumProfileFrame)
		chromiumProfileButton = FrameButton(self, window, text="Account Form", class_frame=AccountFrame)

		UpdateTokenButton = FrameButton(self, window, text="Update Account Token", class_frame=UpdateTokenFrame)
		proxyProfileButton = FrameButton(self, window, text="Proxy Form", class_frame=ProxyFrame)


		# # # layout
		titleLabel.grid(column = 0, row = 0, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotv4Button.grid(column = 0, row = 1, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotcheckButton.grid(column = 0, row = 2, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		resybotbookingButton.grid(column = 0, row = 3, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		reservationlistButton.grid(column = 0, row = 4, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		chromiumProfileButton.grid(column = 0, row = 5, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		UpdateTokenButton.grid(column = 0, row = 6, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)
		proxyProfileButton.grid(column = 0, row = 7, sticky=(W, E, N, S), padx=15, pady=5, columnspan=3)

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
		valuentry = Entry(self, width=180)
		dlist = StringVar(value=RESERVATION_LIST)
		self.valueslist = Listbox(self, width=180, height=10, listvariable=dlist)
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
		profilenamentry = EntryWithPlaceholder(self, width=180, placeholder="Profile Name (Space Not allowed)")
		emailentry = EntryWithPlaceholder(self, width=180, placeholder="Email")
		passwordentry = EntryWithPlaceholder(self, width=180, placeholder="Password")

		dlist = StringVar(value=PROFILE_LIST)
		self.valueslist = Listbox(self, width=180, height=10, listvariable=dlist)
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

class ProxyProfileFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		file = open("proxylist.json", "r")
		self.proxylist = json.load(file)
		PROXY_LIST = [f"{value['profilename']} | {value['http_proxy']} | {value['https_proxy']}" for value in self.proxylist]
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
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
		self.rowconfigure(11, weight=1)
		self.rowconfigure(12, weight=1)

		titleLabel = TitleLabel(self, text="Update Proxy Profile")
		profilenamentry = EntryWithPlaceholder(self, width=180, placeholder="Profile Name (Space is not allowed)")
		httpproxyentry = EntryWithPlaceholder(self, width=180, placeholder="HTTP Proxy: proxy_type://username:password@proxy_address:port_number")
		httpsproxyentry = EntryWithPlaceholder(self, width=180, placeholder="HTTPS Proxy: proxy_type://username:password@proxy_address:port_number")


		dlist = StringVar(value=PROXY_LIST)
		self.valueslist = Listbox(self, width=180, height=10, listvariable=dlist)
		self.valueslist.bind( "<Double-Button-1>" , self.removeValue)
		addButton = ttk.Button(self, text='Add', command = lambda:self.addlist(profilename=profilenamentry, http_proxy=httpproxyentry, https_proxy=httpsproxyentry, valuelist=self.valueslist))
		closeButton = CloseButton(self)
		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S))
		profilenamentry.grid(column = 0, row = 1, sticky=(W))
		httpproxyentry.grid(column = 0, row = 2, sticky=(W))
		httpsproxyentry.grid(column = 0, row = 3, sticky=(W))

		self.valueslist.grid(column = 0, row = 4, sticky=(W))
		addButton.grid(column = 0, row = 1, sticky = (E))
		closeButton.grid(column = 0, row = 4, sticky = (E, S))
	
	def removeValue(self, event):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		selection = self.valueslist.curselection()
		for i in self.valueslist.curselection():
			strselect = self.valueslist.get(i).split(" | ")[0]
			messagebox.showinfo("Message box", f"`{strselect}` deleted..")
		self.valueslist.delete(selection)
		tmplist = []
		for dl in self.proxylist:
			if dl['profilename'] != strselect:
				tmplist.append(dl)
		self.proxylist = tmplist.copy()
		savejson(filename="proxylist.json", valuelist=self.proxylist)

	def addlist(self, **kwargs):
		self.proxylist.append({"profilename": kwargs['profilename'].get(), "http_proxy": kwargs['http_proxy'].get(), "https_proxy": kwargs['https_proxy'].get()})
		if savejson(filename="proxylist.json", valuelist=self.proxylist, value=kwargs['profilename'].get()):
			kwargs['valuelist'].insert(0, f"{kwargs['profilename'].get()} | {kwargs['http_proxy'].get()} | {kwargs['https_proxy'].get()}")
		else:
			# breakpoint()
			self.proxylist.pop()
		
		kwargs['profilename'].delete(0, END)
		kwargs['http_proxy'].delete(0, END)
		kwargs['https_proxy'].delete(0, END)
		
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
		
		profileList = []
		for text in [value for value in db.accountSelectMandatory()]:
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
		profileselected = db.getAccount(email=profile)
		run_module(comlist=[PYLOC, "modules/update_token.py", "-em", profileselected[1], "-pw", profileselected[2]])
				
class ResyBotv5Frame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		self.rowconfigure(12, weight=1)
		self.rowconfigure(13, weight=1)
		
		# populate
		titleLabel = TitleLabel(self, text="Resy Bot Booking Form")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Date: ")
		timelabel = Label(self, text="Time: ")
		rangelabel = Label(self, text="hours before & after: ")
		seatslabel = Label(self, text="Seats: ")
		reservationlabel = Label(self, text="Reservation Type: ")
		chprofilelabel = Label(self, text="Account: ")
		runimlabel = Label(self, text="Run Immediately: ")
		rundatelabel = Label(self, text="Run Date: ")
		runtimelabel = Label(self, text="Run Time: ")
		nstoplabel = Label(self, text="Nonstop Checking: ")
		durationlabel = Label(self, text="Duration in Minutes: ")
		proxylabel = Label(self, text="Proxy: ")
		retrylabel = Label(self, text="Retry Count: ")
		minidlelabel = Label(self, text="Min Idle Time: ")
		maxidlelabel = Label(self, text="Max Idle Time: ")
		# checkonlylabel = Label(self, text="Availability Check Only: ")

		self.url = StringVar(value="https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		urlentry = Entry(self, width=80, textvariable=self.url)
		self.date = StringVar()
		dateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date)
		self.time = StringVar()
		self.timeentry = SpinTimePickerOld(self)
		self.timeentry.addHours12()
		self.timeentry.addMinutes()
		self.timeentry.addPeriod()
		self.defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=self.defseat, state="readonly", width=5)
		# seatsentry.insert(0,2)
		self.defrange = StringVar(value=0)
		rangeentry = Spinbox(self, from_=0, to=100, textvariable=self.defrange, state="readonly", width=5)
		# rangeentry.insert(0,0)
		self.reservation = StringVar()
		reservationentry = ttk.Combobox(self, textvariable=self.reservation, state="readonly", width=30)
		reservationentry['values'] =  db.reservationSelect()
		reservationentry.current(0)
		self.profile=StringVar()
		chprofileentry = ttk.Combobox(self, textvariable=self.profile, state="readonly", width=30)
		chprofileentry['values'] = db.accountSelectMandatory()
		chprofileentry.current(0)
		self.rundate = StringVar()
		rundateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.rundate)
		self.runtimeentry = SpinTimePickerOld(self)
		self.runtimeentry.addHours12()
		self.runtimeentry.addMinutes()
		self.runtimeentry.addSeconds()
		self.runtimeentry.addPeriod()
		self.runim = StringVar()
		runimentry = ttk.Combobox(self, textvariable=self.runim, state="readonly", width=5)
		runimentry['values'] = ['No','Yes']
		runimentry.current(0)
		self.nstop=StringVar()
		nstopentry = ttk.Combobox(self, textvariable=self.nstop, state="readonly", width=5)
		nstopentry['values'] = ['No','Yes']
		nstopentry.current(0)
		# self.checkonly=StringVar()
		# checkonlyentry = ttk.Combobox(self, textvariable=self.checkonly, state="readonly", width=5)
		# checkonlyentry['values'] = ['No','Yes']
		# checkonlyentry.current(0)

		self.duration = StringVar(value=0)
		durationentry = Spinbox(self, from_=0, to=600, textvariable=self.duration, width=5)
		self.proxy=StringVar()
		proxyentry = ttk.Combobox(self, textvariable=self.proxy, state="readonly", width=30)
		proxyentry['values'] = db.proxySelect()
		proxyentry.current(0)
		self.retry = StringVar(value=10)
		retryentry = Spinbox(self, from_=1, to=100, textvariable=self.retry, state="readonly", width=5)
		self.minidle = StringVar(value=1)
		minidleentry = Spinbox(self, from_=1, to=100, textvariable=self.minidle, state="readonly", width=5)
		self.maxidle = StringVar(value=5)
		maxidleentry = Spinbox(self, from_=1, to=100, textvariable=self.maxidle, state="readonly", width=5)

		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(url=urlentry, date=dateentry, time=self.timeentry, seats=seatsentry, reservation=reservationentry, profile=chprofileentry, range_hours=rangeentry, run_date=rundateentry, run_time=self.runtimeentry, runnow=runimentry, nonstop=nstopentry, duration=durationentry, proxy=proxyentry, retry=retryentry, minidle=minidleentry, maxidle=maxidleentry), style="Fancy.TButton")
		runButton = ttk.Button(self, text='Run', command=self.runCommand, style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeCommand, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateCommand, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)
		urllabel.grid(column = 0, row = 1, sticky=(W))
		urlentry.grid(column = 0, row = 1, sticky=(E))
		datelabel.grid(column = 0, row = 2, sticky=(W))
		dateentry.grid(column = 0, row = 2, sticky=(E))
		timelabel.grid(column = 0, row = 3, sticky=(W))
		self.timeentry.grid(column = 0, row = 3, sticky=(E))
		rangelabel.grid(column = 0, row = 4, sticky=(W))
		rangeentry.grid(column = 0, row = 4, sticky=(E))
		seatslabel.grid(column = 0, row = 5, sticky=(W))
		seatsentry.grid(column = 0, row = 5, sticky=(E))
		reservationlabel.grid(column = 0, row = 6, sticky=(W))
		reservationentry.grid(column = 0, row = 6, sticky=(E))
		rundatelabel.grid(column = 0, row = 7, sticky=(W))
		rundateentry.grid(column = 0, row = 7, sticky=(E))
		runtimelabel.grid(column = 0, row = 8, sticky=(W))
		self.runtimeentry.grid(column = 0, row = 8, sticky=(E))
		runimlabel.grid(column = 0, row = 9, sticky=(W))
		runimentry.grid(column = 0, row = 9, sticky=(E))
		chprofilelabel.grid(column = 2, row = 1, sticky=(W))
		chprofileentry.grid(column = 2, row = 1, sticky=(E))
		nstoplabel.grid(column = 2, row = 2, sticky=(W))
		nstopentry.grid(column = 2, row = 2, sticky=(E))
		durationlabel.grid(column = 2, row = 3, sticky=(W))
		durationentry.grid(column = 2, row = 3, sticky=(E))
		proxylabel.grid(column = 2, row = 4, sticky=(W))
		proxyentry.grid(column = 2, row = 4, sticky=(E))
		retrylabel.grid(column = 2, row = 5, sticky=(W))
		retryentry.grid(column = 2, row = 5, sticky=(E))
		minidlelabel.grid(column = 2, row = 6, sticky=(W))
		minidleentry.grid(column = 2, row = 6, sticky=(E))
		maxidlelabel.grid(column = 2, row = 7, sticky=(W))
		maxidleentry.grid(column = 2, row = 7, sticky=(E))
		# checkonlylabel.grid(column = 2, row = 8, sticky=(W))
		# checkonlyentry.grid(column = 2, row = 8, sticky=(E))

		# viewButton.grid(column=2, row=8, sticky=(W))
		saveButton.grid(column = 2, row = 10, sticky = (E))
		runButton.grid(column = 0, row = 10, sticky = (W))
		updateButton.grid(column = 2, row = 10, sticky = (W))
		removeButton.grid(column = 0, row = 10, sticky = (E))
		closeButton.grid(column = 2, row = 12, sticky = (E))
		self.tableOutputFrame()
		self.viewCommand()
		self.resetForm()
                
	def savelist(self, **kwargs):
		formatted_time = convert24time(kwargs['time'])
		formatted_runtime = convert24timeSecond(kwargs['run_time'])
		db.insertCommand(url=kwargs['url'].get(), datewanted=str(kwargs['date'].get_date()), timewanted=formatted_time, seats=kwargs['seats'].get(), reservation=kwargs['reservation'].get(), account=kwargs['profile'].get(), hoursba=kwargs['range_hours'].get(), rundate=str(kwargs['run_date'].get_date()), runtime=formatted_runtime, runnow=kwargs['runnow'].get(), nonstop=kwargs['nonstop'].get(), duration=kwargs['duration'].get(), proxy=kwargs['proxy'].get(), retry=kwargs['retry'].get(), minidle=kwargs['minidle'].get(), maxidle=kwargs['maxidle'].get())
		self.viewCommand()
		messagebox.showinfo("Message box","Booking list Saved")
		self.resetForm()
		
	def viewCommand(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewCommand():
			self.out.insert("", END, values=row)

	def runCommand(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Command Record to Run!")
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				run_module(comlist=[PYLOC, "modules/resybotv5.py", "-u", '{}'.format(item[17]), "-d", '{}'.format(item[2]), "-t", '{}'.format(item[3]), "-s", '{}'.format(item[5]), "-r", '{}'.format(item[6]), "-cp", item[10],  "-rd", '{}'.format(item[7]), "-rt", item[8], "-rh", '{}'.format(item[4]), "-rn", '{}'.format(item[9]), "-ns", '{}'.format(item[11]), "-dr", '{}'.format(item[12]), "-up", '{}'.format(item[13]), "-re", '{}'.format(item[14]), "-mn", '{}'.format(item[15]), "-mx", '{}'.format(item[16])])
		
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Command Record to Run!")

	def removeCommand(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Command Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeCommand(item[0])
			self.resetForm()
			self.viewCommand()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Command Record to Remove!")
		

	def updateCommand(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Bot Command Record to Update!")
			return
		# print(self.url.get())
		formatted_time = convert24time(self.timeentry)
		formatted_runtime = convert24timeSecond(self.runtimeentry)
		# breakpoint()
		db.updateCommand(comid=self.chosenRow[0], url=self.url.get(), datewanted=self.date.get(), timewanted=formatted_time, hoursba=self.defrange.get(), seats=self.defseat.get(), reservation=self.reservation.get(), rundate=self.rundate.get(), runtime=formatted_runtime, runnow=self.runim.get(), account=self.profile.get(), nonstop=self.nstop.get(), duration=self.duration.get(), proxy=self.proxy.get(), retry=self.retry.get(), minidle=self.minidle.get(), maxidle=self.maxidle.get())
		self.viewCommand()
		messagebox.showinfo("Info", "Command Updates..")
		self.resetForm()
		
	def resetForm(self):
		self.url.set("https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		self.date.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
		self.timeentry.set12Hrs(5)
		self.timeentry.setMins(0)
		self.timeentry.setPeriod("p.m")
		self.defseat.set("2")
		self.defrange.set("0")
		self.reservation.set("<Not Set>")
		self.rundate.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
		# self.profile.set(self.chosenRow[10])
		periodrt = datetime.strftime(datetime.now(), "%p").lower()
		periodrt = periodrt[0]+"."+periodrt[1]
		self.runtimeentry.set12Hrs(datetime.strftime(datetime.now(), "%I"))
		self.runtimeentry.setMins(datetime.strftime(datetime.now(), "%M"))
		self.runtimeentry.setSecs(datetime.strftime(datetime.now(), "%S"))
		self.runtimeentry.setPeriod(periodrt)
		# self.runtimeentry.set12Hrs(self.chosenRow[8].split(":")[0])
		self.runim.set("No")
		self.nstop.set("No")
		self.duration.set("0")
		self.proxy.set("<Not Set>")
		self.retry.set("10")
		self.minidle.set("1")
		self.maxidle.set("5")
		# self.checkonly.set("No")

	def tableOutputFrame(self):
		self.tableFrame = Frame(self, bg="#DADDE6")
		# self.tableFrame.place(x=0, y=400, width=1290, height=260)
		self.tableFrame.grid(column=0, row=11, columnspan=3,sticky = (W, E, N, S))
		# titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)

		self.yScroll = Scrollbar(self.tableFrame)
		self.yScroll.pack(side=RIGHT, fill=Y)
		self.style = ttk.Style()
		self.style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")
		self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, 
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18), style="mystyle.Treeview")
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Restaurant")
		self.out.column("2", width=200, stretch="no")
		self.out.heading("3", text="Date")
		self.out.column("3", width=5)
		self.out.heading("4", text="Time")
		self.out.column("4", width=5)
		self.out.heading("5", text="Range")
		self.out.column("5", width=2, anchor="center")
		self.out.heading("6", text="Seats")
		self.out.column("6", width=2, anchor="center")
		self.out.heading("7", text="Reservation")
		self.out.column("7", width=5)
		self.out.heading("8", text="RunDate")
		self.out.column("8", width=5)
		self.out.heading("9", text="RunTime")
		self.out.column("9", width=5) 
		self.out.heading("10", text="RNow") 
		self.out.column("10", width=70, anchor="center", stretch="no")
		self.out.heading("11", text="Account")
		self.out.column("11", width=10)
		self.out.heading("12", text="NStop")
		self.out.column("12", width=70, anchor="center", stretch="no")
		self.out.heading("13", text="Drs")
		self.out.column("13", width=70, anchor="center", stretch="no")
		self.out.heading("14", text="Proxy")
		self.out.column("14", width=10)
		self.out.heading("15", text="Retry")
		self.out.column("15", width=2, anchor="center")
		self.out.heading("16", text="Min")
		self.out.column("16", width=2, anchor="center")
		self.out.heading("17", text="Max")
		self.out.column("17", width=2, anchor="center")
		# self.out.heading("18", text="COnly") 
		# self.out.column("18", width=70, anchor="center", stretch="no")
		self.out.heading("18", text="URL")
		self.out.column("18", width=0, stretch=0)

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		# self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)
		self.out.pack(fill=X)
		self.yScroll.config(command=self.out.yview)

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.url.set(self.chosenRow[17])
			self.date.set(self.chosenRow[2])
			self.timeentry.set12Hrs(self.chosenRow[3].split(":")[0] )
			self.timeentry.setMins(self.chosenRow[3].split(":")[1].split(" ")[0])
			self.timeentry.setPeriod(self.chosenRow[3][-2:].lower()[0] + "." + self.chosenRow[3][-2:].lower()[1])
			self.defseat.set(self.chosenRow[5])
			self.defrange.set(self.chosenRow[4])
			self.reservation.set(self.chosenRow[6])
			self.rundate.set(self.chosenRow[7])
			self.profile.set(self.chosenRow[10])
			self.runtimeentry.set12Hrs(self.chosenRow[8].split(":")[0])
			self.runtimeentry.setMins(self.chosenRow[8].split(":")[1])
			self.runtimeentry.setSecs(self.chosenRow[8].split(":")[-1].split(" ")[0])
			self.runtimeentry.setPeriod(self.chosenRow[8][-2:].lower()[0] + "." + self.chosenRow[8][-2:].lower()[1])
			self.runim.set(self.chosenRow[9])
			self.nstop.set(self.chosenRow[11])
			self.duration.set(self.chosenRow[12])
			self.proxy.set(self.chosenRow[13])
			self.retry.set(self.chosenRow[14])
			self.minidle.set(self.chosenRow[15])
			self.maxidle.set(self.chosenRow[16])
			# self.checkonly.set(self.chosenRow[17])


		except IndexError as error:
			pass

class ResyBotCheckFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		titleLabel = TitleLabel(self, text="Resy Bot Checking Availability Form")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Start Date: ")
		date2label = Label(self, text="End Date: ")
		seatslabel = Label(self, text="Seats: ")
		nstoplabel = Label(self, text="Nonstop Checking: ")
		proxylabel = Label(self, text="Proxy: ")
		minidlelabel = Label(self, text="Min Idle Time: ")
		maxidlelabel = Label(self, text="Max Idle Time: ")
		retryseclabel = Label(self, text="Seconds Between Retries: ")
		self.url = StringVar(value="https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		urlentry = Entry(self, width=80, textvariable=self.url)
		self.date = StringVar()
		dateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date)
		self.date2 = StringVar()
		date2entry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date2)
		self.defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=self.defseat, state="readonly", width=5)
		self.nstop=StringVar()
		nstopentry = ttk.Combobox(self, textvariable=self.nstop, state="readonly", width=5)
		nstopentry['values'] = ['No','Yes']
		nstopentry.current(0)
		self.proxy=StringVar()
		proxyentry = ttk.Combobox(self, textvariable=self.proxy, state="readonly", width=30)
		proxyentry['values'] = db.proxySelect()
		proxyentry.current(0)
		self.minidle = StringVar(value=1)
		minidleentry = Spinbox(self, from_=1, to=100, textvariable=self.minidle, state="readonly", width=5)
		self.maxidle = StringVar(value=5)
		maxidleentry = Spinbox(self, from_=1, to=100, textvariable=self.maxidle, state="readonly", width=5)
		self.retrysec = StringVar(value=0.05)
		retrysecentry = Spinbox(self, format='%.2f', increment=0.01, from_=0.01, to=10.00, textvariable=self.retrysec, state="readonly", width=5)

		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(url=urlentry, date=dateentry, date2=date2entry, seats=seatsentry, nonstop=nstopentry,  proxy=proxyentry, minidle=minidleentry, maxidle=maxidleentry, retrysec=retrysecentry), style="Fancy.TButton")
		runButton = ttk.Button(self, text='Run', command=self.runCheck, style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeCheck, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateCheck, style="Fancy.TButton")
		logButton = ttk.Button(self, text='Show Log', command=self.showLog, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)
		urllabel.grid(column = 0, row = 1, sticky=(W))
		urlentry.grid(column = 0, row = 1, sticky=(E))
		datelabel.grid(column = 0, row = 2, sticky=(W))
		dateentry.grid(column = 0, row = 2, sticky=(E))
		date2label.grid(column = 0, row = 3, sticky=(W))
		date2entry.grid(column = 0, row = 3, sticky=(E))
		seatslabel.grid(column = 0, row = 4, sticky=(W))
		seatsentry.grid(column = 0, row = 4, sticky=(E))
		nstoplabel.grid(column = 2, row = 1, sticky=(W))
		nstopentry.grid(column = 2, row = 1, sticky=(E))
		proxylabel.grid(column = 2, row = 2, sticky=(W))
		proxyentry.grid(column = 2, row = 2, sticky=(E))
		minidlelabel.grid(column = 2, row = 3, sticky=(W))
		minidleentry.grid(column = 2, row = 3, sticky=(E))
		maxidlelabel.grid(column = 2, row = 4, sticky=(W))
		maxidleentry.grid(column = 2, row = 4, sticky=(E))
		retryseclabel.grid(column = 2, row = 5, sticky=(W))
		retrysecentry.grid(column = 2, row = 5, sticky=(E))

		saveButton.grid(column = 2, row = 6, sticky = (N, E))
		runButton.grid(column = 0, row = 6, sticky = (N, W))
		updateButton.grid(column = 2, row = 6, sticky = (N, W))
		removeButton.grid(column = 0, row = 6, sticky = (N,E))
		closeButton.grid(column = 2, row = 8, sticky = (E))
		logButton.grid(column = 1, row = 6, sticky = (N))

		self.tableOutputFrame()
		self.viewCheck()
		self.resetForm()
                
	def savelist(self, **kwargs):
		db.insertCheck(url=kwargs['url'].get(), startdate=str(kwargs['date'].get_date()), enddate=str(kwargs['date2'].get_date()), seats=kwargs['seats'].get(), nonstop=kwargs['nonstop'].get(),  proxy=kwargs['proxy'].get(), minidle=kwargs['minidle'].get(), maxidle=kwargs['maxidle'].get(), retrysec=kwargs['retrysec'].get())
		self.viewCheck()
		messagebox.showinfo("Message box","Checking Availability list Saved")
		self.resetForm()
		
	def viewCheck(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewCheck():
			self.out.insert("", END, values=row)
		
	def runCheck(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Checking Availability Record to Run!")
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				# filelog = open(f"logs/checking_stdout_{item[0]}.log", "w")
				# comlist=[PYLOC, "modules/resybotcheck1.py", "-u", '{}'.format(item[10]), "-sd", '{}'.format(item[2]), "-ed", '{}'.format(item[3]), "-s", '{}'.format(item[4]), "-up", '{}'.format(item[6]), "-ns", '{}'.format(item[5]), "-id", '{}'.format(item[0]), "-mn", '{}'.format(item[7]), "-mx", '{}'.format(item[8]), "-rs", '{}'.format(item[9])]
				comlist=[PYLOC, "modules/resybotcheck1.py", "-id", '{}'.format(item[0])]
				run_module(comlist=comlist)
				# proc=Popen(comlist, creationflags=CREATE_NEW_CONSOLE, stdout=filelog)
				# proc=Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
				
				# proc=Popen(comlist)

				# print(proc.pid)
				# for line in proc.stdout:
				# 	sys.stdout.write(line)
				# 	filelog.write(line)
				# proc.wait()
				# run_module(comlist=comlist)
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Run!")
		except Exception as e:
			messagebox.showerror("Error!", str(e))

	def removeCheck(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Checking Availability Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeCheck(item[0])
			self.resetForm()
			self.viewCheck()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Remove!")
		

	def updateCheck(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Update!")
			return
		db.updateCheck(comid=self.chosenRow[0], url=self.url.get(), startdate=self.date.get(), enddate=self.date2.get(), seats=self.defseat.get(), nonstop=self.nstop.get(), proxy=self.proxy.get(), minidle=self.minidle.get(), maxidle=self.maxidle.get(), retrysec=self.retrysec.get())
		self.viewCheck()
		messagebox.showinfo("Info", "Check Availability Updates..")
		self.resetForm()
		
	def showLog(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability to show the Log File!")
			return
		self.viewCheck()
		logfile = f"logs/checking_{self.chosenRow[0]}.log"
		if Path(logfile).exists():
			Popen(["notepad.exe", logfile])
		else:
			messagebox.showerror("Error!", "File Not Found")
		self.resetForm()

	def resetForm(self):
		self.url.set("https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		self.date.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
		self.date2.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))

		self.defseat.set("2")
		self.nstop.set("No")
		self.proxy.set("<Not Set>")
		self.minidle.set("10")
		self.maxidle.set("60")
		self.retrysec.set("0.5")


	def tableOutputFrame(self):
		self.tableFrame = Frame(self, bg="#DADDE6")
		# self.tableFrame.place(x=0, y=400, width=1290, height=260)
		self.tableFrame.grid(column=0, row=7, columnspan=3,sticky = (W, E, N, S))
		# titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)

		self.yScroll = Scrollbar(self.tableFrame)
		self.yScroll.pack(side=RIGHT, fill=Y)
		self.style = ttk.Style()
		self.style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")
		self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, 
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), style="mystyle.Treeview")
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Restaurant")
		self.out.column("2", width=200, stretch="no")
		self.out.heading("3", text="Start Date")
		self.out.column("3", width=5, anchor="center")
		self.out.heading("4", text="End Date")
		self.out.column("4", width=5, anchor="center")
		self.out.heading("5", text="Seats")
		self.out.column("5", width=2, anchor="center")
		self.out.heading("6", text="NStop")
		self.out.column("6", width=70, anchor="center", stretch="no")
		self.out.heading("7", text="Proxy")
		self.out.column("7", width=10, anchor="center")
		self.out.heading("8", text="Min Idle")
		self.out.column("8", width=2, anchor="center")
		self.out.heading("9", text="Max Idle")
		self.out.column("9", width=2, anchor="center")
		self.out.heading("10", text="Secs Retry")
		self.out.column("10", width=2, anchor="center")
		self.out.heading("11", text="URL")
		self.out.column("11", width=0, stretch=0)

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		# self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)
		self.out.pack(fill=X)
		self.yScroll.config(command=self.out.yview)

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.url.set(self.chosenRow[10])
			self.date.set(self.chosenRow[2])
			self.date2.set(self.chosenRow[3])
			self.defseat.set(self.chosenRow[4])
			self.nstop.set(self.chosenRow[5])
			self.proxy.set(self.chosenRow[6])
			self.minidle.set(self.chosenRow[7])
			self.maxidle.set(self.chosenRow[8])
			self.retrysec.set(self.chosenRow[9])

		except IndexError as error:
			pass

class RerservationFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		titleLabel = TitleLabel(self, text="Reservation Form")
		# titleLabel =Label(self, text="Reservation Form")
		namelabel = Label(self, text="Name: ")
		self.name = StringVar()
		nameentry = Entry(self, width=60, textvariable=self.name)

		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(name=nameentry), style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeData, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateData, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 1, sticky = (W, E, N), padx=30)
		namelabel.grid(column = 0, row = 2, sticky=(W,N))
		nameentry.grid(column = 0, row = 2, sticky=(E,N), padx=30)

		saveButton.grid(column = 0, row = 3, sticky = (N, E), padx=30)
		updateButton.grid(column = 0, row = 3, sticky = (N))
		removeButton.grid(column = 0, row = 3, sticky = (N,W))
		closeButton.grid(column = 2, row = 10, sticky = (E))

		self.tableOutputFrame()
		self.viewData()
		self.resetForm()
                
	def savelist(self, **kwargs):
		db.insertReservation(name=kwargs['name'].get())
		self.viewData()
		messagebox.showinfo("Message box","Reservation list Saved")
		self.resetForm()
		
	def viewData(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewReservation():
			self.out.insert("", END, values=row)
		

	def removeData(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Reservation Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeReservation(item[0])
			self.resetForm()
			self.viewData()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Reservation Record to Remove!")
		
	def updateData(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Reservation Record to Update!")
			return
		db.updateReservation(comid=self.chosenRow[0], name=self.name.get())
		self.viewData()
		messagebox.showinfo("Info", "Reservation Updates..")
		self.resetForm()

	def resetForm(self):
		self.name.set("")


	def tableOutputFrame(self):
		style = ttk.Style()
		style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky=(W))
		self.out = ttk.Treeview(self,  columns=(1,2), style="mystyle.Treeview", height=200)
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Type Name")
		self.out.column("2", width=200, stretch="yes")

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		self.out.grid(column=1, row=1, rowspan=4, columnspan=2, pady=30, sticky=(W, E, N, S))

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.name.set(self.chosenRow[1])

		except IndexError as error:
			pass

class AccountFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		titleLabel = TitleLabel(self, text="Account Form")
		emaillabel = Label(self, text="Email: ")
		self.email = StringVar()
		emailentry = Entry(self, width=60, textvariable=self.email)
		passwordlabel = Label(self, text="Password: ")
		self.password = StringVar()
		passwordentry = Entry(self, width=60, textvariable=self.password)
		paymentlabel = Label(self, text="Payment Method ID: ")
		self.payment = StringVar()
		paymententry = Entry(self, width=60, textvariable=self.payment)


		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(email=emailentry, password=passwordentry, payment=paymententry), style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeData, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateData, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 1, sticky = (W, E, N), padx=30)
		emaillabel.grid(column = 0, row = 2, sticky=(W,N))
		emailentry.grid(column = 0, row = 2, sticky=(E,N), padx=30)
		passwordlabel.grid(column = 0, row = 3, sticky=(W,N))
		passwordentry.grid(column = 0, row = 3, sticky=(E,N), padx=30)
		paymentlabel.grid(column = 0, row = 4, sticky=(W,N))
		paymententry.grid(column = 0, row = 4, sticky=(E,N), padx=30)

		saveButton.grid(column = 0, row = 5, sticky = (N, E), padx=30)
		updateButton.grid(column = 0, row = 5, sticky = (N))
		removeButton.grid(column = 0, row = 5, sticky = (N,W))
		closeButton.grid(column = 2, row = 10, sticky = (E))

		self.tableOutputFrame()
		self.viewData()
		self.resetForm()
                

	def savelist(self, **kwargs):
		db.insertAccount(email=kwargs['email'].get(),password=kwargs['password'].get(),token='', payment_method_id=kwargs['payment'].get(), api_key='')
		self.viewData()
		messagebox.showinfo("Message box","Account list Saved")
		self.resetForm()
		
	def viewData(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewAccount():
			self.out.insert("", END, values=row)
		

	def removeData(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Account Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeAccount(item[0])
			self.resetForm()
			self.viewData()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Account Record to Remove!")
		
	def updateData(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Account Record to Update!")
			return
		db.updateAccount(comid=self.chosenRow[0], email=self.email.get(), password=self.password.get(), token=self.chosenRow[3], api_key=self.chosenRow[4], payment_method_id=self.payment.get())
		self.viewData()
		messagebox.showinfo("Info", "Account Updates..")
		self.resetForm()

	def resetForm(self):
		self.email.set("")
		self.password.set("")
		self.payment.set("")

	def tableOutputFrame(self):
		style = ttk.Style()
		style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky=(W))
		self.out = ttk.Treeview(self,  columns=(1,2,3,4,5,6), style="mystyle.Treeview", height=200)
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Email")
		self.out.column("2", width=100, stretch="yes")
		self.out.heading("3", text="Password")
		self.out.column("3", width=100, stretch="yes")
		self.out.heading("4", text="Token")
		self.out.column("4", width=0, stretch="no")
		self.out.heading("5", text="API Key")
		self.out.column("5", width=0, stretch="no")
		self.out.heading("6", text="Payment Method ID")
		self.out.column("6", width=100, stretch="yes")

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		self.out.grid(column=1, row=1, rowspan=8, columnspan=2, pady=30, sticky=(W, E, N, S))

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.email.set(self.chosenRow[1])
			self.password.set(self.chosenRow[2])
			self.payment.set(self.chosenRow[5])

		except IndexError as error:
			pass

class ProxyFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		titleLabel = TitleLabel(self, text="Proxy Form")
		namelabel = Label(self, text="Name: ")
		self.name = StringVar()
		nameentry = Entry(self, width=60, textvariable=self.name)
		httplabel = Label(self, text="Http: ")
		self.http = StringVar()
		httpentry = Entry(self, width=60, textvariable=self.http)
		httpslabel = Label(self, text="Https: ")
		self.https = StringVar()
		httpsentry = Entry(self, width=60, textvariable=self.https)


		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(name=nameentry, http=httpentry, https=httpsentry), style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeData, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateData, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 1, sticky = (W, E, N), padx=30)
		namelabel.grid(column = 0, row = 2, sticky=(W,N))
		nameentry.grid(column = 0, row = 2, sticky=(E,N), padx=30)
		httplabel.grid(column = 0, row = 3, sticky=(W,N))
		httpentry.grid(column = 0, row = 3, sticky=(E,N), padx=30)
		httpslabel.grid(column = 0, row = 4, sticky=(W,N))
		httpsentry.grid(column = 0, row = 4, sticky=(E,N), padx=30)

		saveButton.grid(column = 0, row = 5, sticky = (N, E), padx=30)
		updateButton.grid(column = 0, row = 5, sticky = (N))
		removeButton.grid(column = 0, row = 5, sticky = (N,W))
		closeButton.grid(column = 2, row = 10, sticky = (E))

		self.tableOutputFrame()
		self.viewData()
		self.resetForm()
                

	def savelist(self, **kwargs):
		db.insertProxy(name=kwargs['name'].get(),http=kwargs['http'].get(), https=kwargs['https'].get())
		self.viewData()
		messagebox.showinfo("Message box","Proxy list Saved")
		self.resetForm()
		
	def viewData(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewProxy():
			self.out.insert("", END, values=row)
		

	def removeData(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Proxy Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeProxy(item[0])
			self.resetForm()
			self.viewData()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Proxy Record to Remove!")
		
	def updateData(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Proxy Record to Update!")
			return
		db.updateProxy(comid=self.chosenRow[0], name=self.name.get(), http=self.http.get(), https=self.https.get())
		self.viewData()
		messagebox.showinfo("Info", "Proxy Updates..")
		self.resetForm()

	def resetForm(self):
		self.name.set("")
		self.http.set("")
		self.https.set("")

	def tableOutputFrame(self):
		style = ttk.Style()
		style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky=(W))
		self.out = ttk.Treeview(self,  columns=(1,2,3,4), style="mystyle.Treeview", height=200)
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Name")
		self.out.column("2", width=100, stretch="yes")
		self.out.heading("3", text="HTTP")
		self.out.column("3", width=100, stretch="yes")
		self.out.heading("4", text="HTTPS")
		self.out.column("4", width=100, stretch="yes")

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		# self.out.bind("<Up>", self.getData)
		# self.out.bind("<Down>", self.getData)

		self.out.grid(column=1, row=1, rowspan=8, columnspan=2, pady=30, sticky=(W, E, N, S))

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.name.set(self.chosenRow[1])
			self.http.set(self.chosenRow[2])
			self.https.set(self.chosenRow[3])

		except IndexError as error:
			pass

class ResyBotBookingFrame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

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
		titleLabel = TitleLabel(self, text="Resy Bot Checking Availability and Booking Form")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Start Date: ")
		date2label = Label(self, text="End Date: ")
		seatslabel = Label(self, text="Seats: ")
		nstoplabel = Label(self, text="Nonstop Checking: ")
		proxylabel = Label(self, text="Proxy: ")
		minidlelabel = Label(self, text="Min Idle Time: ")
		maxidlelabel = Label(self, text="Max Idle Time: ")
		retryseclabel = Label(self, text="Seconds Between Retries: ")
		timelabel = Label(self, text="Time Wanted: ")
		rangelabel = Label(self, text="hours before & after: ")
		reservationlabel = Label(self, text="Reservation Type: ")
		accountlabel = Label(self, text="Account: ")

		self.url = StringVar(value="https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		urlentry = Entry(self, width=70, textvariable=self.url)
		self.date = StringVar()
		dateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date)
		self.date2 = StringVar()
		date2entry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date2)
		self.defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=self.defseat, state="readonly", width=5)
		self.nstop=StringVar()
		nstopentry = ttk.Combobox(self, textvariable=self.nstop, state="readonly", width=5)
		nstopentry['values'] = ['No','Yes']
		nstopentry.current(0)
		self.proxy=StringVar()
		proxyentry = ttk.Combobox(self, textvariable=self.proxy, state="readonly", width=30)
		proxyentry['values'] = db.proxySelect()
		proxyentry.current(0)
		self.minidle = StringVar(value=1)
		minidleentry = Spinbox(self, from_=1, to=100, textvariable=self.minidle, state="readonly", width=5)
		self.maxidle = StringVar(value=5)
		maxidleentry = Spinbox(self, from_=1, to=100, textvariable=self.maxidle, state="readonly", width=5)
		self.retrysec = StringVar(value=0.05)
		retrysecentry = Spinbox(self, format='%.2f', increment=0.01, from_=0.01, to=10.00, textvariable=self.retrysec, state="readonly", width=5)
		self.defrange = StringVar(value=0)
		rangeentry = Spinbox(self, from_=0, to=100, textvariable=self.defrange, state="readonly", width=5)
		self.reservation = StringVar()
		reservationentry = ttk.Combobox(self, textvariable=self.reservation, state="readonly", width=30)
		reservationentry['values'] =  db.reservationSelect()
		reservationentry.current(0)
		self.account=StringVar()
		accountentry = ttk.Combobox(self, textvariable=self.account, state="readonly", width=30)
		accountentry['values'] = db.accountSelect()
		accountentry.current(0)
		self.time = StringVar()
		self.timeentry = SpinTimePickerOld(self)
		self.timeentry.addHours12()
		self.timeentry.addMinutes()
		self.timeentry.addPeriod()


		style = ttk.Style()
		# style.theme_use("clam")
		style.configure("Fancy.TButton", font=("Cooper Black", 12), foreground="blue", background="green")

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert', command = lambda:self.savelist(url=urlentry, date=dateentry, date2=date2entry, seats=seatsentry, nonstop=nstopentry,  proxy=proxyentry, minidle=minidleentry, maxidle=maxidleentry, retrysec=retrysecentry, account=accountentry, reservation=reservationentry, timewanted=self.timeentry, hoursba=rangeentry), style="Fancy.TButton")
		runButton = ttk.Button(self, text='Run', command=self.runCheckBooking, style="Fancy.TButton")
		removeButton = ttk.Button(self, text='Delete', command=self.removeCheckBooking, style="Fancy.TButton")
		updateButton = ttk.Button(self, text='Update', command=self.updateCheckBooking, style="Fancy.TButton")
		logButton = ttk.Button(self, text='Show Log', command=self.showLog, style="Fancy.TButton")

		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)
		urllabel.grid(column = 0, row = 1, sticky=(W))
		urlentry.grid(column = 0, row = 1, sticky=(E), padx=10)
		datelabel.grid(column = 0, row = 2, sticky=(W))
		dateentry.grid(column = 0, row = 2, sticky=(E), padx=10)
		date2label.grid(column = 0, row = 3, sticky=(W))
		date2entry.grid(column = 0, row = 3, sticky=(E), padx=10)
		seatslabel.grid(column = 0, row = 4, sticky=(W))
		seatsentry.grid(column = 0, row = 4, sticky=(E), padx=10)
		nstoplabel.grid(column = 1, row = 1, sticky=(W))
		nstopentry.grid(column = 1, row = 1, sticky=(E), padx=10)
		proxylabel.grid(column = 1, row = 2, sticky=(W))
		proxyentry.grid(column = 1, row = 2, sticky=(E), padx=10)
		minidlelabel.grid(column = 1, row = 3, sticky=(W))
		minidleentry.grid(column = 1, row = 3, sticky=(E), padx=10)
		maxidlelabel.grid(column = 1, row = 4, sticky=(W))
		maxidleentry.grid(column = 1, row = 4, sticky=(E), padx=10)
		retryseclabel.grid(column = 1, row = 5, sticky=(W))
		retrysecentry.grid(column = 1, row = 5, sticky=(E), padx=10)

		timelabel.grid(column = 2, row = 1, sticky=(W))
		self.timeentry.grid(column = 2, row = 1, sticky=(E))
		rangelabel.grid(column = 2, row = 2, sticky=(W))
		rangeentry.grid(column = 2, row = 2, sticky=(E))
		reservationlabel.grid(column = 2, row = 3, sticky=(W))
		reservationentry.grid(column = 2, row = 3, sticky=(E))
		accountlabel.grid(column = 2, row = 4, sticky=(W))
		accountentry.grid(column = 2, row = 4, sticky=(E))

		saveButton.grid(column = 2, row = 6, sticky = (N, E))
		runButton.grid(column = 0, row = 6, sticky = (N, W))
		updateButton.grid(column = 2, row = 6, sticky = (N, W))
		removeButton.grid(column = 0, row = 6, sticky = (N,E), padx=10)
		closeButton.grid(column = 2, row = 8, sticky = (E))
		logButton.grid(column = 1, row = 6, sticky = (N))

		self.tableOutputFrame()
		self.viewCheckBooking()
		self.resetForm()
                
	def savelist(self, **kwargs):
		formatted_time = convert24time(kwargs['timewanted'])
		db.insertCheckBooking(url=kwargs['url'].get(), startdate=str(kwargs['date'].get_date()), enddate=str(kwargs['date2'].get_date()), seats=kwargs['seats'].get(), account=kwargs['account'].get(), timewanted=formatted_time, hoursba=kwargs['hoursba'].get(), reservation=kwargs['reservation'].get(), nonstop=kwargs['nonstop'].get(),  proxy=kwargs['proxy'].get(), minidle=kwargs['minidle'].get(), maxidle=kwargs['maxidle'].get(), retrysec=kwargs['retrysec'].get())
		self.viewCheckBooking()
		messagebox.showinfo("Message box","Checking Availability list Saved")
		self.resetForm()
		
	def viewCheckBooking(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewCheckBooking():
			self.out.insert("", END, values=row)
		
	def runCheckBooking(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Checking Availability Record to Run!")
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				# filelog = open(f"logs/checking_stdout_{item[0]}.log", "w")
				comlist=[PYLOC, "modules/resybotcheckbooking1.py", "-id", '{}'.format(item[0])]
				run_module(comlist=comlist)
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Run!")
		except Exception as e:
			messagebox.showerror("Error!", str(e))

	def removeCheckBooking(self):
		selection = self.out.selection()
		if len(selection) == 0:
			messagebox.showerror("Error!", "Please Choose a Bot Checking Availability Record to Delete!")
			return

		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			for i in selection:
				item = self.out.item(i)['values']
				db.removeCheckBooking(item[0])
			self.resetForm()
			self.viewCheckBooking()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Remove!")
		

	def updateCheckBooking(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability Record to Update!")
			return
		db.updateCheckBooking(comid=self.chosenRow[0], url=self.url.get(), startdate=self.date.get(), enddate=self.date2.get(), seats=self.defseat.get(), account=self.account.get(), timewanted=self.time.get(), hoursba=self.defrange.get(), reservation=self.reservation.get(), nonstop=self.nstop.get(), proxy=self.proxy.get(), minidle=self.minidle.get(), maxidle=self.maxidle.get(), retrysec=self.retrysec.get())
		self.viewCheckBooking()
		messagebox.showinfo("Info", "Check Availability Updates..")
		self.resetForm()
		
	def showLog(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose a Bot Check Availability to show the Log File!")
			return
		self.viewCheckBooking()
		logfile = f"logs/checkbooking_{self.chosenRow[0]}.log"
		if Path(logfile).exists():
			Popen(["notepad.exe", logfile])
		else:
			messagebox.showerror("Error!", "File Not Found")
		self.resetForm()

	def resetForm(self):
		self.url.set("https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		self.date.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
		self.date2.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
		self.timeentry.set12Hrs(5)
		self.timeentry.setMins(0)
		self.timeentry.setPeriod("p.m")
		self.defseat.set("2")
		self.defrange.set("0")
		self.reservation.set("<Not Set>")
		self.nstop.set("No")
		self.proxy.set("<Not Set>")
		self.minidle.set("10")
		self.maxidle.set("60")
		self.retrysec.set("0.5")

	def tableOutputFrame(self):
		self.tableFrame = Frame(self, bg="#DADDE6")
		self.tableFrame.grid(column=0, row=7, columnspan=3,sticky = (W, E, N, S))

		self.yScroll = Scrollbar(self.tableFrame)
		self.yScroll.pack(side=RIGHT, fill=Y)
		self.style = ttk.Style()
		self.style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=25)
		self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")
		self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, 
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), style="mystyle.Treeview")
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Restaurant")
		self.out.column("2", width=200, stretch="no")
		self.out.heading("3", text="Start Date")
		self.out.column("3", width=5, anchor="center")
		self.out.heading("4", text="End Date")
		self.out.column("4", width=5, anchor="center")
		self.out.heading("5", text="Seats")
		self.out.column("5", width=2, anchor="center")
		self.out.heading("6", text="Account")
		self.out.column("6", width=10, anchor="center")
		self.out.heading("7", text="Time Wanted")
		self.out.column("7", width=5, anchor="center")
		self.out.heading("8", text="Range")
		self.out.column("8", width=2, anchor="center")
		self.out.heading("9", text="Reservation")
		self.out.column("9", width=10, anchor="center")
		self.out.heading("10", text="NStop")
		self.out.column("10", width=10, anchor="center")
		self.out.heading("11", text="Proxy")
		self.out.column("11", width=10, anchor="center")
		self.out.heading("12", text="Min Idle")
		self.out.column("12", width=2, anchor="center")
		self.out.heading("13", text="Max Idle")
		self.out.column("13", width=2, anchor="center")
		self.out.heading("14", text="Secs Retry")
		self.out.column("14", width=2, anchor="center")
		self.out.heading("15", text="URL")
		self.out.column("15", width=0, stretch=0)

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		# self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)
		self.out.pack(fill=X)
		self.yScroll.config(command=self.out.yview)

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.url.set(self.chosenRow[14])
			self.date.set(self.chosenRow[2])
			self.date2.set(self.chosenRow[3])
			self.defseat.set(self.chosenRow[4])
			self.account.set(self.chosenRow[5])
			self.time.set(self.chosenRow[6])
			self.defrange.set(self.chosenRow[7])
			self.reservation.set(self.chosenRow[8])
			self.nstop.set(self.chosenRow[9])
			self.proxy.set(self.chosenRow[10])
			self.minidle.set(self.chosenRow[11])
			self.maxidle.set(self.chosenRow[12])
			self.retrysec.set(self.chosenRow[13])

		except IndexError as error:
			pass

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
		proc = Popen(comlist)
	elif platform == "win32":
		proc = Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
		print(proc.pid)

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
