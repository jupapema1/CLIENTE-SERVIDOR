#server.py
#10.253.26.52
import sys
import zmq
import json
import hashlib
import time 
import os

partSize = 1024 * 1024 * 10

def generateCode():
    pass

def downloadFile3(filename, socket, ID, folder):
    print("Filename: {}".format(filename[0].decode()))
    fl=filename[0].decode()
    newName="./"+folder+'/'+ID.decode()+"-"+fl
    print("Downloading [{}]".format(newName))
    with open(newName, "rb") as f:
        finished = False
        part = 0
        while not finished:
            print("Uploading part {}".format(part+1))

            f.seek(part*partSize)
            bt = f.read(partSize)
            socket.send_multipart([fl.encode(), bt])


            #print("Received reply [%s]" % (response))
            
            part = part + 1
            
            if len(bt) < partSize:
                finished = True

        #print("Waiting for ok...")
        #response = socket.recv()
        print("Downloaded!!")

def start():
    if len(sys.argv) != 2:
        print("Must be called with a folder name")
        print("Sample call: python server.py <location>")
        exit()
    loc=sys.argv[1]

    if os.path.isdir('./'+loc) == False:
        print("Creating directory.../{}".format(loc))
        os.mkdir('./'+loc)    

    print ("Running server...")

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    port="5555"
    socket.bind("tcp://*:5555")

    while True:
        #print("Running server in port: ")
        #  Wait for next request from client
        print("\nWaiting message from client...\n")
        ident, message,*rest = socket.recv_multipart()
        print("Received request: %s" % message.decode())   
        if message.decode()=='up':
            print("Operation: Upload File...")
            filename,info=rest
            newName=loc+'/'+ident.decode()+'-'+filename.decode()
            print("Storing as [{}]".format(newName))
            with open(newName,"wb") as f:
                f.write(info)
            socket.send(b"OK")
            print("Uploaded as [{}]".format(newName))
        elif message.decode()=="down":
            print("Operation: Download File...")
            filename=rest
            downloadFile3(filename, socket, ident,loc)

        elif message.decode()=="bye":
            exit()

        #time.sleep(5)
        #socket.send(b"OK")
        #print("socket: {}".format())
        print("Replied!")


def main():
    print ("Running server...")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    port="5555"
    socket.bind("tcp://*:5555")

    while True:
        #print("Running server in port: ")
        #  Wait for next request from client
        message = socket.recv_json()
        print("Received request: %s" % message)

        #  Do some 'work'
        #time.sleep(1)

        #  Send reply back to client

        socket.send(b"{'bye'}")


if __name__ == '__main__':
    start()
