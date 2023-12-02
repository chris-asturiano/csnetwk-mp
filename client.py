import socket
import ast

def send_file(client_socket, filename):
    with open(filename, 'rb') as file:
        data = file.read(3145728)
        client_socket.send(data)
        file.close()
        
def receive_file(client_socket, filename):
    with open(filename, 'wb') as file:
        data = client_socket.recv(3145728)
        file.write(data)
        file.flush()
        file.close()

joined = False
registered = False


while True:
    # prompt the user for input
    print("Type \"/?\" for help")
    user_input = input("Enter your input: ")


    # get first word of input
    command = user_input.split()[0]

    if command == '/join':
        if len(user_input.split()) == 3 and user_input.split()[2].isdigit():
            HOST = str(user_input.split()[1])
            PORT = int(user_input.split()[2])
            print('Trying to connect...')
            
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))
                # send message to server
                print('Connection to the File Exchange Server is successful!')
                joined = True
            except:
                print('Error: Connection to the Server has failed! Please check IP Address and Port Number.')
                
        else:
            print('Error: Command parameters do not match or is not allowed.')
            
    elif command == '/leave':
        try:
            if joined:
                client.sendall(bytes("/leave", 'utf-8'))
                reply = client.recv(3145728)
                print(reply.decode("utf-8"))
                
                client.close()
                joined = False
                registered = False
                
            else:
                print('Error: You are not connected to any server!')
                
        except:
            print('Error: Server not responding!')
            
    elif command == '/register':
        try:
            if len(user_input.split()) != 2:
                print('Error: Command parameters do not match or is not allowed.')
                
            else:
                if not joined:
                    print('Error: You are not connected to any server!')
                    
                else:
                    client.sendall(bytes(user_input, 'utf-8'))
                    reply = client.recv(3145728)
                    print(reply.decode("utf-8"))
                    message = reply.decode("utf-8")
                    
                    if message.split()[0] == 'Successfully':
                        registered = True
                    else:
                        registered = False
        except:
            print('Error: Server not responding!')
        
    elif command == '/store':
        try: 
            if not joined:
                print('Error: You are not connected to any server!')
                
            elif not registered:
                print('You are currently not registered.')
                continue
            
            else:
                # send file to server
                client.sendall(bytes(user_input, 'utf-8'))
                filename = user_input.split()[1]
                send_file(client, filename)
                print("Done Sending")
                
        except:
            print('Error: Server not responding!')
          
    elif command == '/dir':
        try:
            if not joined:
                print('Error: You are not connected to any server!')
                
            elif not registered:
                print('You are currently not registered.')
                
            else:
                client.sendall(bytes("/dir", 'utf-8'))
                data = client.recv(3145728)
                if not data:
                    break
                message = data.decode("utf-8")
                message = ast.literal_eval(message)
                print('\nServer Directory:')
                if message == []:
                    print('No files in directory!')
                for i in range(len(message)):
                    print(message[i])
                print()
                
        except:
            print('Error: Server not responding!')

    elif command == '/get':
        if not joined:
            print('Error: You are not connected to any server!')
            
        elif not registered:
            print('You are currently not registered.')
            
        else: 
            client.sendall(bytes(user_input, 'utf-8'))
            filename = user_input.split()[1]
            reply = client.recv(3145728)
            message = reply.decode("utf-8")
            
            if message == 'File not found!':
                print('Error: File not found in the server.')
                
            else:
                receive_file(client, filename)
                print('File received from Server: ' + filename)
    elif command == '/?':
        lines = '------------------------------------------------------------------------------------------------------------------------'
        print()
        print(lines)
        print('%-45s %-45s %-42s' % ('Description', '|   Input Syntax', '|   Sample Input Script'))
        print(lines)
        print('%-45s %-45s %-42s' % ('Connect to the server application', '|   /join <server_ip_add> <port>', '|   /join 192.168.1.1 12345'))
        print('%-45s %-45s %-42s' % ('Disconnect to the server application', '|   /leave', '|   /leave'))
        print('%-45s %-45s %-42s' % ('Register a unique handle or alias', '|   /register <handle>', '|   /register User1'))
        print('%-45s %-45s %-42s' % ('Send file to server', '|   /store <filename>', '|   /store Hello.txt'))
        print('%-45s %-45s %-42s' % ('Request directory file list from a server', '|   /dir', '|   /dir'))
        print('%-45s %-45s %-42s' % ('Fetch a file from a server', '|   /get <filename>', '|   /get Hello.txt'))
        print(lines)
        print()
    else:
        print('Error: Command not found.')

