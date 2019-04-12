#cliente.py
import zmq
import json 
import sys


partSize = 1024 * 1024 * 10


def writeBytes(filename,info):
    newName='new-'+filename
    print("Writing file...[{}]".format(newName))

    with open(newName,"wb") as f:
        f.write(info)
    print("Downloaded [{}]".format(newName))

def uploadFile2(filename, socket, ID):
    with open(filename, "rb") as f:
        finished = False
        part = 0
        while not finished:
            print("Uploading part {}".format(part+1))

            f.seek(part*partSize)
            bt = f.read(partSize)
            socket.send_multipart([ID, b"up",filename, bt])

            #print("Received reply [%s]" % (response))
            
            part = part + 1
            
            if len(bt) < partSize:
                finished = True

        #print("Waiting for ok...")
        response = socket.recv()
        if response.decode()=='OK':
            print("Uploaded!")
        else: 
            print("Error!")

def downloadFile(filename,socket,ID):
    #print("Download not implemented yet!!!!")
    socket.send_multipart([ID,b'down',filename])
    response=socket.recv_multipart()
    filename,info=response
    print("write[{}]".format(filename))
    writeBytes(filename.decode(),info)

    


def main():

    if len(sys.argv) != 4:
        print("Must be called with a filename")
        print("Sample call: python client.py <identification> <operation> <filename>")
        exit()

    ident= sys.argv[1].encode()
    operation = sys.argv[2].encode()
    filename = sys.argv[3].encode()

    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting with server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    #socket.send_json({'1':'0'})
    #socket.send_multipart([operation,filename])

    if operation.decode()=='up':
        uploadFile2(filename,socket, ident)
    elif operation.decode()=='down':
        downloadFile(filename,socket,ident)

    #message = socket.recv_multipart()
    #print("Received reply [ %s ]" % (message[0].decode()))



if __name__ == '__main__':
    main()