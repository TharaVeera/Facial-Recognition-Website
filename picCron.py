import os
import sqlite3

directory = 'dataset'
pathToDatabase =  r"C:\sqlite\customerData.db"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        datasetPath = r'C:\Desktop\Streaming\dataset' + '\\' + filename
        #print("hi", fullPath)
        id = int(os.path.split(filename)[-1].split(".")[1])
        #print(id)
        CID = "C" + str(id)
        #print(CID)
        conn = sqlite3.connect(pathToDatabase)
        c = conn.cursor()
        c.execute("DELETE FROM picBackup;")
        #c.execute("INSERT INTO picBackup (PID) VALUES (" + fullPath + ");")
        #custValuesStr = "'" + custID + "', '" + name + "', '" + company + "'"
        #visitsValuesStr = "'" + custID + "', '" + date + "', '" + time + "', '1'" #date, time, num of visits
        picValuesStr = "'" + CID + "','" + datasetPath + "'"
        c.execute("INSERT INTO picBackup (CID, PID) VALUES (" + picValuesStr + ");")
        #c.execute("INSERT INTO custInfo (CID, Name, Company) VALUES (" + custValuesStr + ");")
        #c.execute("INSERT INTO Visits (CID, Date, Time, totalVisits) VALUES (" + visitsValuesStr + ");")
        conn.commit()
        conn.close()