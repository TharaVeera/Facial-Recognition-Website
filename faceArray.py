# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:39:36 2018

@author: 1023191
"""
import sqlite3 
import os

class faceArray(object):
    pathToDatabase = None
    def __init__(self):
        self.pathToDatabase = r"C:\sqlite\customerData.db"
        
    def repopArray(self):
        nameArray = []
        conn = sqlite3.connect(self.pathToDatabase)
        c = conn.cursor()
        c.execute("SELECT Name FROM custInfo;")
        nameArray = nameArray[:] + [r[0] for r in c.fetchall()]
        print("nameArray: ", nameArray)
        conn.commit()
        conn.close()
        return nameArray
    
    def repopArrayNotFromDB(self):
        nameArray = ["None", "Prachi", "Sara", "Jack", "Tyler", "Tristan", "Bailey" ]
        return nameArray

    def addtoArray(self, name):
        #name = [ [name, company]]
        nameArray = self.repopArray()
        nameArray.append(name)
        print (nameArray)
        #customerID = len(name_companyArray) -1;
        #print(name_companyArray, customerID)
        
    def getNewCID(self):
        nameArray = self.repopArray()
        ID = len(nameArray)
        CID = "C" + str(ID)
        return CID
    
    def deleteFromTempImages(self): 
        folderTempImages = 'tempImages'
        for file in os.listdir(folderTempImages):
            filePath = os.path.join(folderTempImages, file)
            try: 
                if os.path.isfile(filePath):
                    if "manifest" not in filePath:
                        os.unlink(filePath)
            except Exception as e:
                print(e)
                pass
            