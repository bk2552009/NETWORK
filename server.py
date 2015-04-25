__author__ = 'spacewalker'
import socket
import threading
import os

def ServerFunction(name, sock, addr):
    while True:
        getfilemode = sock.recv(1024) #recv 1
        if getfilemode[:3] == "get":
            filepath = getfilemode.split( )
            fileToDownload = filepath.pop()
            if os.path.isfile(fileToDownload):
                sock.send("EXISTS" + str(os.path.getsize(fileToDownload)))
                userResponse = sock.recv(1024)
                if userResponse[:2] == 'OK':
                    with open(fileToDownload, 'rb') as f:
                        bytesTosend = f.read(1024)
                        sock.send(bytesTosend)
                        while bytesTosend != "":
                            bytesTosend = f.read(1024)
                            sock.send(bytesTosend)
                        print "Client has downloaded " + fileToDownload
        elif getfilemode == "uploadmode":
            filename = sock.recv(1024) #recv 2
            cutfilename = os.path.split(filename)
            filesize = sock.recv(1024) #recv 1.5
            #filename = sock.recv(1024) #recv 2
            f = open('new_ul_'+cutfilename[1], 'wb') #file extendsion is gone!!! NOT FIX YET
            data = sock.recv(1024) #recv 3
            totalRecv = len(data)
            f.write(data)
            while totalRecv < int(filesize):
                data = sock.recv(1024)
                totalRecv += len(data)
                f.write(data)
                #print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
            #uploadedFile = sock.recv(1024)
            print "Upload Complete!\n" + "Client has uploaded: " + filename
            f.close()
        elif getfilemode == "listremotemode":
            filepath = sock.recv(1024)
            filepath = filepath.split( )
            filepath = filepath.pop()
            path = filepath
            print "File lists in local directory: " + os.path.basename(path)
            dirs = os.listdir(path)
            filecount = len(dirs)
            sock.send(str(filecount))
            for files in dirs:
                sock.send(files)
            print "Files in directory " + os.path.basename(path) + " were sent to client"
            '''elif getfilemode == "exit":
            print "Client " + "<"+addr+">" + "had been disconnected!"
            sock.close()
            t.stop()'''
        else:
            sock.send("Error! There is no command that you want...")
    sock.close()

def Main():
    host = ""
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print "Server start ..."
    while True:
        c, addr = s.accept()
        print 'There is a connection from', addr
        t = threading.Thread(target=ServerFunction, args=("RetrThread", c, addr))
        t.start()
    t.stop()
    s.close()

if __name__ == '__main__':
    Main()