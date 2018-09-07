# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:19:55 2018

@author: 1023191
"""

import sqlite3
from time import strftime

class DAO(object):
    pathToDatabase = None
    def __init__(self):
        self.pathToDatabase = r"C:\sqlite\customerData.db"
   
    def insertToCustInfo(self, CID, name, company):
        conn = sqlite3.connect(self.pathToDatabase)
        c = conn.cursor()
        custValuesStr = "'" + CID + "', '" + name + "', '" + company + "'"
        c.execute("INSERT INTO custInfo (CID, Name, Company) VALUES (" + custValuesStr + ");")
        conn.commit()  
        conn.close()        
        
    def insertToVisits(self, CID):
        conn = sqlite3.connect(self.pathToDatabase)
        c = conn.cursor()
        date = strftime("%Y-%m-%d ") 
        time = strftime("%H:%M:%S")
        visitsValuesStr = "'" + CID + "', '" + date + "', '" + time + "', '1'"  
        c.execute("INSERT INTO Visits (CID, Date, Time, totalVisits) VALUES (" + visitsValuesStr + ");")
        conn.commit()  
        conn.close()        
        
        
    def updateVisits(self, CID):
        conn = sqlite3.connect(self.pathToDatabase)
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
        date = strftime("%Y-%m-%d ") 
        time = strftime("%H:%M:%S")
        c.execute("SELECT totalVisits FROM Visits WHERE CID='"+ CID+"';")
        totalVisits = [r[-1] for r in c.fetchall()]
        print(totalVisits)
        totalVisits = str(totalVisits[-1])
        print ("totalVisits ", totalVisits)
        visitsUpdate = int(totalVisits) + 1
        visitsValuesStr = "'"+ CID + "', '" + date + "', '" + time + "', '" + str(visitsUpdate)+"'"
        print(visitsValuesStr)
        c.execute("INSERT INTO Visits (CID, Date, Time, totalVisits) VALUES (" + visitsValuesStr + ");")
        conn.commit()  
        conn.close() 
        
    #def updateLinkedIn
    #def insertToLinkedIn
        