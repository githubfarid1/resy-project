from pathlib import Path
import os
PYTHON_EXE = os.getcwd() + os.sep + r"venv\Scripts\python.exe"
RESY_EMAIL='scuffedcookery@gmail.com'
RESY_PASSWORD='Upworktest1!'
HEADLESS='no'
CLOSE_MESSAGE=" --> Press any key to close..."
tmplist = ["Table", "Dining Room", "Bar", "Bar Counter", "Kitchen Counter", "Table (Not Bar)", "Side table(not bar)", "Patio", "Street Seating", "WHISKY ROOM", "SUSHI COUNTER", "High Top", "Bar Mutsumi", "Bar Seat", "Omakase Bar", "Side Table (Not Sushi Bar)", "Sushi Counter", "counter"]
setlist = set(tmplist)
RESERVATION_LIST = list(setlist)
RESERVATION_LIST.sort()
PERIOD_LIST = ["Dinner", "Lunch", "Brunch"]