from flask import Flask, render_template, session, Response, request, redirect, url_for, stream_with_context
from DAO import DAO
from faceArray import faceArray
from socketForImageData import socketForImageData
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)
app.secret_key = "supplychain4lyfe"
#http://10.0.8.166:5000 on linux

@app.route('/')
def index():
    closeSocket = socketForImageData()
    closeSocket.endConnection()
    session.pop('name', None)
    session.pop('company', None)
    session.pop('CID', None)
    cache.clear()
    faces = faceArray()
    faces.deleteFromTempImages() #This folder has the temporary picture for the welcome page
    
    return render_template('start.html')

@app.route("/yes/", methods=['GET'])
def yes(): 
    #new = true
    return render_template('yes.html')

@app.route("/yes/streamFD/", methods=['POST'])
def yesNames():
    
    name = request.form['Name']
    session['name'] = name
    
    company = request.form['Company']
    session['company'] = company
    
    newCustomer = faceArray();
    CID = newCustomer.getNewCID()
    #print("CID ", CID)
    session['CID'] =  CID #C# for testing
    cache.set('myCID', CID)
    
    newCustomerDAO = DAO()
    newCustomerDAO.insertToCustInfo(CID, name, company)
    newCustomerDAO.insertToVisits(CID)
    
    #Begin listening on the socket 
    #newCustomerSocket = socketForImageData()
    #newCustomerSocket.receiveImageData()
    
    return render_template('streamFD.html', name = name, company = company)

@app.route('/streamFD')
def streamFD():
    return render_template('streamFD.html')
    
@app.route("/welcome/", methods=['GET'])
def welcome(): 
    customerSocket = socketForImageData()
    customerSocket.endConnection()
    #FOR NEW CUSTOMER
    if 'name' in session: 
        print("name is in seesion")
        name = session['name'] #ALREADY UPDATED IN YESNAME
    #FOR OLD CUSTOMER
    else:
        print("name is not in session")
        name = cache.get('myname')
        CID = cache.get('myCID')
        if(name != None and CID != None):
            print("name in cache")
            print("CID: " + CID)
            print("Name: " + name)
            welcomeCustomerDAO = DAO() 
            welcomeCustomerDAO.updateVisits(CID)
         
        else:
            print("name not in cache")
            name = ""
            CID = "C0" #unknown visitor 
            welcomeCustomerDAO = DAO()
            welcomeCustomerDAO.updateVisits(CID)
        

    return render_template('welcome.html', name = name)

@app.route("/welcomeUK/", methods=['GET'])
def welcomeUK():
    
    UKCustomerSocket = socketForImageData()
    UKCustomerSocket.endConnection()
    
    print("unknown customer")
    #name = ""
    CID = "C0" #unknown visitor 
    welcomeCustomerDAO = DAO()
    welcomeCustomerDAO.updateVisits(CID)
    return render_template('welcomeUK.html')
    

@app.route("/no/", methods=['GET'])
def noFR(): 
    #endconnection
    oldCustomerSocket = socketForImageData()
    oldCustomerSocket.endConnection() #BEWARE: There is a lag here! Can result in socket closing error. 

    #cache.set('myname', None)
    #cache.set('myCID', None)
    cache.clear()
    return render_template('isthisYou.html')

@app.route("/restartFR/", methods=['GET'])
def restartFR(): 
    #oldCustomerSocket = socketForImageData()
    #oldCustomerSocket.endConnection()
    cache.clear()
    print( cache.get('myname'))
    print(cache.get('myCID'))
    return render_template('restartFR.html')
 
     
def genFacialDetection(newCustomerSocket):#camera1
    print("DOING FACIAL DETECTION")
    CID = cache.get('myCID')
    print("MYCID: ", CID)
    face_id = CID[1:]
    count = 1

    while (count < 40):
        frame = newCustomerSocket.receiveImageDataFD(count, int(face_id))
        if(frame is not None):
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            count = count +1

    newCustomerSocket.endConnection()
    #cache.clear()
        
@app.route('/video_feed')
def video_feedFD():
    newCustomerSocket = socketForImageData()
    socketSuccess = newCustomerSocket.beginConnection()
    if socketSuccess:
        return Response(stream_with_context(genFacialDetection(newCustomerSocket)),#socketForImageData()
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        print("Cannot perform facial detection and livestream images")
        return
    
def genFacialRecognition(oldCustomerSocket):

    print("DOING FACIAL RECOGNITION")
    count = 1
    id = 0
    name = ""
    while (count < 100):
       id, name, frame = oldCustomerSocket.receiveImageDataFR(count)
       #frame = oldCustomerSocket.receiveImageDataFR()
       if(name is not None or id is not None):
           CID = "C" + str(id)
           print("name ", name, "CID ", CID)
           cache.set('myname', name)
           cache.set('myCID', CID)
       if(frame is not None):
           yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  
           count +=1
    oldCustomerSocket.endConnection()


@app.route('/video_feed2')
def video_feedFR():

    oldCustomerSocket = socketForImageData()
    socketSuccess = oldCustomerSocket.beginConnection()
    if socketSuccess:
        return Response(stream_with_context(genFacialRecognition(oldCustomerSocket)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        print("Cannot perform facial recognition and livestream images")
        return

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
