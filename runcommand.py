from subprocess import Popen, check_call, call
import psutil
fname = open("logs/command1.log", "w")
process = Popen(["python", "modules/resybotv5.py", "-u", "https://resy.com/cities/new-york-ny/venues/coqodaq", "-d", "2024-08-19", "-t", "5:00 PM", "-s", "2", "-r", "<Not Set>", "-cp", "resyfarid2@proton.me", "-rd", "2024-08-17", "-rt", "8:51:38 PM", "-rh", "0", "-rn", "Yes", "-ns", "Yes", "-dr", "0", "-up", "new_proxy", "-re", "10", "-mn", "5", "-mx", "10"
], stdout=fname)
