__author__ = 'spacewalker'
import socket
import threading
import os
from os import path


host = '127.0.0.1'
port = 5000
s = socket.socket()
s.connect((host, port))
print "Connected...\n" + "COMMAND\n" + "1) ls = list file in directory\n"\
      + "2) lls = list file in remote directory\n" + "3) get = download file\n"\
      + "4) put = upload file\n"
while True:
    command = raw_input("Please Enter Command here: ")
    if command[:2] == 'ls': #ls command
        filepath = command.split( )
        if len(filepath) < 2:
            print 'Invalid Command. ls or lls need 2 arguments which are ls <filepath> or lls <filepath>'
            break
        else:
            filepath = filepath.pop()
        path = filepath
        print "Files list in remote directory: " + os.path.basename(path)
        dirs = os.listdir(path)
        for files in dirs:
            print "- " +files
    elif command[:3] == 'lls': #lls command
        s.send('listremotemode')#send 1
        s.send(command) #send 2
        filecount = s.recv(1024)
        print "Files list from server"
        for i in range(0, int(filecount)):
            fileFromServer = s.recv(1024)
            print fileFromServer

    elif command[:3] == 'get': #get command
        s.send(command)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File exists, " + str(filesize) + "Bytes, download? " \
                                                                   "(Y/N)? -> ")
            if message == 'Y':
                s.send("OK")
                filename = os.path.split(command)
                f = open('new_dl_'+filename[1], 'wb') #file extendsion is gone!!! NOT FIX YET
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                print "Download Complete!"
                f.close()
        else:
            print "File doesn't exist!"
    elif command[:3] == 'put': #get command #s.send(command)
        s.send('uploadmode') #send 1
        filepath = command.split( )
        filepath = filepath.pop()
        fileToUpload = filepath
        if os.path.isfile(fileToUpload):
            uploadSize = os.path.getsize(fileToUpload)
            s.send(str(uploadSize)) #send1.5
            s.send(command) #send 2
            message = raw_input("File Exists! " + str(uploadSize) + " Bytes, upload? "
                                                                    "Y/N? -> ")
            if message == 'Y':
                with open(fileToUpload, 'rb') as f:
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend) #send
                    totalSend = bytesToSend
                    while bytesToSend != "":
                        bytesToSend = f.read(1024)
                        s.send(bytesToSend)
                    print "Upload Complete!"
        '''elif command[:4] == 'exit': #exit command
            s.send("exit")
            print "You have disconnected from server..."
            break'''
    else:
        print "INVALID COMMAND!"
        break
s.close()
