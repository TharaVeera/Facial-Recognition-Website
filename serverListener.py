
  
 import socket 
 import subprocess
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.bind(('172.16.31.79', 5020))
 s.listen(10)

 while True: 
 	conn, addr = s.accept()
 	data = conn.recv(1024)
 	conn.close()
 	subprocess.call(['./sendImages.sh'])