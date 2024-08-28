import sqlite3
import os
import sys
import json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class Database:
    def __init__(self, db):
        # creating database connection
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        # SQL queries to create tables
        sql = """
        CREATE TABLE IF NOT EXISTS commands (
            id Integer PRIMARY KEY,
            url text,
            datewanted text,
            timewanted text,
            hoursba Integer,
            seats Integer,
            reservation text,
            rundate text,
            runtime text,
            runnow text,
            account text,
            nonstop text,
            duration Integer,
            proxy text,
            retry Integer,
            minidle Integer,
            maxidle Integer
        )
        """
        # cursor executions
        self.cur.execute(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS checks (
            id Integer PRIMARY KEY,
            url text,
            startdate text,
            enddate text,
            seats Integer,
            nonstop text,
            proxy text,
            minidle Integer,
            maxidle Integer,
            retrysec Real
        )
        """
        self.cur.execute(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS checkbookings (
            id Integer PRIMARY KEY,
            url text,
            startdate text,
            enddate text,
            seats Integer,
            account text,
            timewanted text,
            hoursba Integer,
            reservation text,
            nonstop text,
            proxy text,
            minidle Integer,
            maxidle Integer,
            retrysec Real
        )
        """
        self.cur.execute(sql)


        sql = """
        CREATE TABLE IF NOT EXISTS reservations (
            id Integer PRIMARY KEY,
            name text
        )
        """
        self.cur.execute(sql)

        sql = """
        CREATE TABLE IF NOT EXISTS proxies (
            id Integer PRIMARY KEY,
            name text,
            http text,
            https text            
        )
        """
        self.cur.execute(sql)


        sql = """
        CREATE TABLE IF NOT EXISTS accounts (
            id Integer PRIMARY KEY,
            email text,
            password text,
            token text,
            api_key text,            
            payment_method_id Integer
        )
        """
        self.cur.execute(sql)
        self.con.commit()


    def reservationValues(self):
        file = open("reservationlist.json", "r")
        listvalue = json.load(file)
        tmplist = [value for value in listvalue]
        tmplist.append("<Not Set>")
        setlist = set(tmplist)
        return sorted(list(setlist), key=str.casefold)

    def proxyValues(self):
        file = open("proxylist.json", "r")
        listvalue = json.load(file)
        tmplist = [value['profilename'] for value in listvalue]
        tmplist.append("<Not Set>")
        setlist = set(tmplist)
        return sorted(list(setlist), key=str.casefold)
    
    def proxyValues2(self):
        file = open("proxylist.json", "r")
        listvalue = json.load(file)
        tmplist = [value for value in listvalue]
        tmplist.append({"profilename":"<Not Set>","http_proxy":'',"https_proxy":""})
        return tmplist
        # setlist = set(tmplist)
        # return sorted(list(setlist), key=str.casefold)

    def profileValues(self):
        file = open("profilelist.json", "r")
        self.profilelist = json.load(file)
        return [value['email'] for value in self.profilelist]

    def profileValues2(self):
        file = open("profilelist.json", "r")
        self.profilelist = json.load(file)
        return [value for value in self.profilelist]

    def insertCommand(self, url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle):
        self.cur.execute("INSERT INTO commands VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle))
        self.con.commit()


    def viewCommand(self):
        self.cur.execute("SELECT * FROM commands order by id desc")
        rows = self.cur.fetchall()
        dlist = []
        for row in rows:
            rowlist = list(row)
            rowlist.append(rowlist[1]) 
            rowlist[1] = rowlist[1].split("/")[-1]
            dlist.append(tuple(rowlist))
        return dlist

    def removeCommand(self, comid):
        self.cur.execute("DELETE FROM commands WHERE id=?", (comid,))
        self.con.commit()

    def updateCommand(self, comid, url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle):
        sql_insert_query = """UPDATE commands SET url=?, datewanted=?, timewanted=?, hoursba=?, seats=?, reservation=?, rundate=?, runtime=?, runnow=?, account=?, nonstop=?, duration=?, proxy=?, retry=?, minidle=?, maxidle=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle, comid))
        self.con.commit()


    def insertCheck(self, url, startdate, enddate, seats, nonstop, proxy, minidle, maxidle, retrysec):
        self.cur.execute("INSERT INTO checks VALUES (NULL,?,?,?,?,?,?,?,?,?)",
                         (url, startdate, enddate, seats, nonstop, proxy, minidle, maxidle, retrysec))
        self.con.commit()

    def viewCheck(self):
        self.cur.execute("SELECT * FROM checks order by id desc")
        rows = self.cur.fetchall()
        dlist = []
        for row in rows:
            rowlist = list(row)
            rowlist.append(rowlist[1]) 
            rowlist[1] = rowlist[1].split("/")[-1]
            dlist.append(tuple(rowlist))
        return dlist

    def removeCheck(self, comid):
        self.cur.execute("DELETE FROM checks WHERE id=?", (comid,))
        self.con.commit()

    def updateCheck(self, comid, url, startdate, enddate, seats, nonstop, proxy, minidle, maxidle, retrysec):
        sql_insert_query = """UPDATE checks SET url=?, startdate=?, enddate=?, seats=?, nonstop=?, proxy=?, minidle=?, maxidle=?, retrysec=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (url, startdate, enddate, seats, nonstop, proxy, minidle, maxidle, retrysec, comid))
        self.con.commit()

    def getCheck(self, id):
        self.cur.execute("SELECT * FROM checks where id=?", (id,))
        return self.cur.fetchone()

    def insertReservation(self, name):
        # breakpoint()
        self.cur.execute("INSERT INTO reservations VALUES (NULL,?)", (name,)) #kalau gak dikasih koma diakhir maka dianggap bukan tuple
        self.con.commit()

    def viewReservation(self):
        self.cur.execute("SELECT * FROM reservations order by name")
        rows = self.cur.fetchall()
        return rows

    def reservationSelect(self):
        self.cur.execute("SELECT name FROM reservations order by name")
        results = []
        for rec in self.cur.fetchall():
            results.append(rec[0]) 
        return results

    def removeReservation(self, comid):
        self.cur.execute("DELETE FROM reservations WHERE id=?", (comid,))
        self.con.commit()

    def updateReservation(self, comid, name):
        sql_insert_query = """UPDATE reservations SET name=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (name, comid))
        self.con.commit()

    def insertProxy(self, name, http, https):
        self.cur.execute("INSERT INTO proxies VALUES (NULL,?,?,?)",
                         (name, http, https))
        self.con.commit()

    # Display Instructor List from table
    def viewProxy(self):
        self.cur.execute("SELECT * FROM proxies order by id desc")
        rows = self.cur.fetchall()
        return rows

    def proxySelect(self):
        self.cur.execute("SELECT name FROM proxies order by name")
        results = []
        for rec in self.cur.fetchall():
            results.append(rec[0]) 
        return results

    def getProxy(self, name):
        self.cur.execute("SELECT * FROM proxies where name=?", (name,))
        return self.cur.fetchone()
    
    def removeProxy(self, comid):
        self.cur.execute("DELETE FROM proxies WHERE id=?", (comid,))
        self.con.commit()

    def updateProxy(self, comid, name, http, https):
        sql_insert_query = """UPDATE proxies SET name=?, http=?, https=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (name, http, https, comid))
        self.con.commit()

    def insertAccount(self, email, password, token, api_key, payment_method_id):
        self.cur.execute("INSERT INTO accounts VALUES (NULL,?,?,?,?,?)",
                         (email, password, token, api_key, payment_method_id))
        self.con.commit()

    def viewAccount(self):
        self.cur.execute("SELECT * FROM accounts order by email desc")
        rows = self.cur.fetchall()
        return rows

    def accountSelect(self):
        self.cur.execute("SELECT email FROM accounts order by email")
        results = []
        for rec in self.cur.fetchall():
            results.append(rec[0]) 
        return results
    
    def accountSelectMandatory(self):
        self.cur.execute("SELECT email FROM accounts WHERE email <> '<Not Set>' order by email")
        results = []
        for rec in self.cur.fetchall():
            results.append(rec[0]) 
        return results

    def getAccount(self, email):
        self.cur.execute("SELECT * FROM accounts where email=?", (email,))
        return self.cur.fetchone()

    def removeAccount(self, comid):
        self.cur.execute("DELETE FROM accounts WHERE id=?", (comid,))
        self.con.commit()

    def updateAccount(self, comid, email, password, token, api_key, payment_method_id):
        sql_insert_query = """UPDATE accounts SET email=?, password=?, token=?, api_key=?, payment_method_id=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (email, password, token, api_key, payment_method_id, comid))
        self.con.commit()

    def insertCheckBooking(self, url, startdate, enddate, seats, account, timewanted, hoursba, reservation, nonstop, proxy, minidle, maxidle, retrysec):
        self.cur.execute("INSERT INTO checkbookings VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (url, startdate, enddate, seats, account, timewanted, hoursba, reservation, nonstop, proxy, minidle, maxidle, retrysec))
        self.con.commit()

    def viewCheckBooking(self):
        self.cur.execute("SELECT * FROM checkbookings order by id desc")
        rows = self.cur.fetchall()
        dlist = []
        for row in rows:
            rowlist = list(row)
            rowlist.append(rowlist[1]) 
            rowlist[1] = rowlist[1].split("/")[-1]
            dlist.append(tuple(rowlist))
        return dlist

    def removeCheckBooking(self, comid):
        self.cur.execute("DELETE FROM checkbookings WHERE id=?", (comid,))
        self.con.commit()

    def updateCheckBooking(self, comid, url, startdate, enddate, seats, account, timewanted, hoursba, reservation, nonstop, proxy, minidle, maxidle, retrysec):
        sql_insert_query = """UPDATE checkbookings SET url=?, startdate=?, enddate=?, seats=?, account=?, timewanted=?, hoursba=?, reservation=?, nonstop=?, proxy=?, minidle=?, maxidle=?, retrysec=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (url, startdate, enddate, seats, account, timewanted, hoursba, reservation, nonstop, proxy, minidle, maxidle, retrysec, comid))
        self.con.commit()

    def getCheckBooking(self, id):
        self.cur.execute("SELECT * FROM checkbookings where id=?", (id,))
        return self.cur.fetchone()
