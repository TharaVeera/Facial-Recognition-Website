# Facial-Recognition-Website
README

This is a Flask Web App that inserts to and updates a database as facial detection and facial recognition occur. 

Set up: 
1. Have a raspberry pi with openCV downloaded on it. Tutorial for downloading openCV: https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
2. Put sendImages.sh, client.py, and serverListener.py on pi. Replace the IP address with yours (the computer running main.py) in client.py.
If pi's IP address has changed, replace the IP address in serverListener.py.
	-The current path to run client.py is in home/pi/Desktop/TestStreaming, which is written in the sendImages.sh file. Change this line of code to where
	you want to store client.py
3. On your server, the one that runs main.py and loads the website, download anaconda with python version 3.6.
4. Then, download openCV, flask, and requests with anaconda:
	-conda install -c conda-forge opencv 
	-conda install -c anaconda flask 
	-conda install -c anaconda requests
5. Download sqlite3 according to this tutorial: http://www.sqlitetutorial.net/download-install-sqlite/
6. Place the customerData.db file in your sqlite folder (change paths on faceArray and DAO if necessary).
7. Follow the cronWindowsInstructions.txt to make picCron.py and facetraining.py cron jobs. It is recommended you run them every day at midnight. 
8. Follow the chromeImagesInstructions.txt to configure the chrome extension to diplay images on the website. Add the extension key provided by chrome
to the templates/welcomeUK and templates/welcome html files. 
9. You should be able to to run the main.py from anaconda with "python main.py"
10. Make sure to run the serverListener.py script on the pi before running the main script on the local computer with: "python serverListener.py". 
11. To run the main script: open an anaconda prompt, type in python main.py. 
12. Then, type in localhost:5000 into chrome. 


Scripts explained: <br/>
-client.py - Live streams video to your computer <br/>
-DAO.py - Represents the Data Access Object. Inserts/Updates to database upon facial detection and facial recognition. <br/>
-faceArray.py - Creates the array of names attached to customer. Also allows you to get a new ID when there is a new customer. <br/>
-facedataset.py - NOT used in main.py. It takes pictures and stores them without using the main website. Can be run separately. <br/>
-facetraining.py - NOT used in main.py, but used as a cron job. Can be run separately to train over pictures. <br/>
-haarcascade_frontalface_default - You will need this in your src folder to do any kind of facial detection/recogntion. <br/>
-linkedin.py- INCOMPLETE. NOT used in main.py Explores the default LinkedIn API. Don't use any github LinkedIn libraries; they don't work.<br/>
-picCron.py - NOT used in main.py, but used as a cron job. This uploads references to pictures stored on computer to the database. <br/>
-sendImages.sh - This is a shell script run on the pi. When the local website wants to begin livestream, it triggers serverListener.py to run. <br/>
-serverListener.py - This must always be running on the pi to work. It listens for the local website to send a signal to start the livestream. <br/>
It calls a subprocess to run sendImages.sh<br/>
-socketForImageData.py - This is where the facial detection and facial recognition scripts are located. A socket connection is "created" every time the website<br/>
performs detection or recognition. It will create a connection with the pi to trigger sendImages.sh to run. It will then receive the stream of image data and unpack it. It will then run that data through the facial recogntion or detection phase depending on what the customer chooses. <br/>
-updateWithInitialData.py - NOT used in main.py. This was used for the demo so no exceptions were caused if it tried to recognize without having any initial data. <br/>
<br/>
Folders explained: <br/>
-dataset- This is where the facial detection phase stores the images for each customer. <br/>
-static - This is where the css file and the images are stored for the website. <br/>
-tempImages - This folder is used to store a temporary image of a customer to put on the welcome pages. It is deleted when the website returns to home. <br/>
-templates - This is where all the templates/web pages are stored for the website. <br/>
-trainer - This is the output from the facetraining.py file. It is read during the face recognition phase.<br/>
