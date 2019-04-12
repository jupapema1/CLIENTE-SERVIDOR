import zmq
import sys
import time

def main():
	if len(sys.argv) != 4:
		print("Error 404")
		exit()
	# recogiendo datos de conexion
	ip = sys.argv[1] #ip servidor
	port = sys.argv[2]	#puerto
	operation = sys.argv[3] # operacion a realizar

	context = zmq.Context()# creamos un contexto
	s = context.socket(zmq.REQ) #crear socket
	s.connect("tcp://{}:{}".format(ip, port)) # conectar al server  por medio de tcp
	# mostramos un mensaje de confirmacion
	print("Connecting to server {} at {}".format(ip, port))
	if operation == "list":	#cliente.py localhost port op
		s.send_json({"op": "list"})# hacemos la peticion al servidor
		files = s.recv_json() #esperando.. info //suspen si no hay nada en el socket
		print(files)
	elif operation == "download":
		name = input("File to download? ")
		s.send_json({"op": "fileparts", "file": name})
		m = s.recv_json()
		if m["info"] != "File not found":
			c = 0
			with open("new_{}".format(name), "wb") as output:
				while c < (int(m["info"])):
					s.send_json({"op": "download", "file": name, "parts": c})
					d = s.recv()
					output.write(d)
					c+=1
		else:
			print("Error, {} {}".format(name,m["info"]))
			exit()
	else: # si la operacion no existe
		print("Error!!!, unsupported operation")

if __name__ == '__main__':
	main()
