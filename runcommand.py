from subprocess import Popen, check_call, call
from sys import platform
if platform == "linux" or platform == "linux2":
    pyexe = "python"
elif platform == "win32":
    pyexe = "venv/Scripts/python.exe"  
fname = open("logs/command1.log", "w")
process = Popen([pyexe, "modules/resybotv5b.py", "-u", "https://resy.com/cities/new-york-ny/venues/coqodaq", "-d", "2024-08-19", "-t", "5:00 PM", "-s", "2", "-r", "<Not Set>", "-cp", "resyfarid2@proton.me", "-rd", "2024-08-17", "-rt", "8:51:38 PM", "-rh", "0", "-rn", "Yes", "-ns", "Yes", "-dr", "0", "-up", "new_proxy", "-re", "10", "-mn", "5", "-mx", "10"
], stdout=fname)
print(process.pid)
