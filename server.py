import socket
import os
from os import listdir
from os.path import isfile, join
import threading
import datetime

def receive_file(server_socket, filename):
    with open(filename, 'wb') as file:
        data = server_socket.recv(3145728)
        file.write(data)
        file.flush()
        file.close()
        

def send_file(server_socket, filename):
    with open(filename, 'rb') as file:
        data = file.read(3145728)
        server_socket.send(data)
        file.close()
                
            
users = []

# function to handle a client
def handle_client(clientsocket, address):
    name = 'Unregistered'  
    print(f"Connection from {address} has been established!")
    i = 0
    while True:
        data = clientsocket.recv(3145728)
        
        if not data:
            break
        
        message = data.decode("utf-8")
        mypath = os.getcwd()
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
        print('From: ' + name + '<' + str(datetime.datetime.now()) + '>' + ': ' + message)
        
        if message.split()[0] == '/dir':
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            onlyfiles.remove('server.py')
            print(onlyfiles)
            clientsocket.sendall(bytes(str(onlyfiles), 'utf-8'))
            
        if message.split()[0] == '/leave':
            clientsocket.sendall(bytes("Connection closed. Thank you!", 'utf-8'))
            clientsocket.close()
            print(f"Connection from {address} has been closed!")
            break
        
        if message.split()[0] == '/register':
            name = message.split()[1]
            
            if name not in users:
                users.append(name)
                print(f'User {name} has been registered!')
                clientsocket.sendall(bytes(f'Successfully registered, welcome {name}!', 'utf-8'))
                
            else:
                print(f'User {name} already exists!')
                clientsocket.sendall(bytes(f'User {name} already exists!', 'utf-8'))
                
        if message.split()[0] == '/store':
            # store file from client
            filename = message.split()[1]
            receive_file(clientsocket, filename)
            print(str(name) + '<' + str(datetime.datetime.now()) + '>' + ': Uploaded ' + message.split()[1])

        if message.split()[0] == '/get':
            # send file to client
            onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            onlyfiles.remove('server.py')
            filename = message.split()[1]
            
            if filename not in onlyfiles:
                print('File not found!')
                clientsocket.sendall(bytes('File not found!', 'utf-8'))
            else: 
                clientsocket.sendall(bytes('Successfully sent the file', 'utf-8'))
                send_file(clientsocket, filename)
                print('Successfully sent the file')
                

# Get file list from directory


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 12345))
s.listen(5)
print("Server is up and running!")
while True:
    clientsocket, address = s.accept()
    # craete new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, address))
    client_thread.start()
