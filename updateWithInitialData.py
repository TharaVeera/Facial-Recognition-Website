# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 09:37:55 2018

@author: 1023191
"""

#NOT UPLOADED FROM DATABASE, THIS IS JUST FOR THE DEMO
#nameArray= ["Unkown", "Thara", "David", "Tony", "Prachi","Tristan", "Hari", "Tyler", "Owen"]
nameArray = ["Unknown", "Prachi", "Sara", "Jack", "Tyler", "Tristan", "Bailey"]

#totalVisitsArray = [0, 0, 0, 0, 0, 0, 0, 0, 0]

import sqlite3
from time import gmtime, strftime

#def updateCustInfo():
pathToDatabase = r"C:\sqlite\customerData.db"
conn = sqlite3.connect(pathToDatabase)
c = conn.cursor()
i = 0
for name in nameArray:
    CID = "C" + str(i)
    if i == 0: 
    	company = "Unknown"
    else:
    	company = "JDA"
    custValuesStr = "'" + CID + "', '" + name + "', '" + company + "'"
    c.execute("INSERT INTO custInfo (CID, Name, Company) VALUES (" + custValuesStr + ");")
    i = i +1
conn.commit()
conn.close()
    #c.execute("SELECT totalVisits FROM Visits WHERE CID='"+ CID+"';")
    #totalVisits = [r[0] for r in c.fetchall()]
#def updateVisits():
pathToDatabase = r"C:\sqlite\customerData.db"
conn = sqlite3.connect(pathToDatabase)
c = conn.cursor()

i = 0
for name in nameArray:
    CID = "C" + str(i)
    date = strftime("%Y-%m-%d ") 
    time = strftime("%H:%M:%S")
    visitsValuesStr = "'" + CID + "', '" + date + "', '" + time + "', '1'" #date, time, num of visits
    c.execute("INSERT INTO Visits (CID, Date, Time, totalVisits) VALUES (" + visitsValuesStr + ");")
    i = i+1

conn.commit()  
conn.close()
    
#updating the pictures is in the picCron script
    

#if __name__ == '__main__':
    