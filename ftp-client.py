import socket
import os

IP = '127.0.0.1'

PORT = 12345

sock = socket.socket()
sock.connect((IP, PORT))
print("Введите логин: ")
try:
    while True:
        request = input('>')
        if request == '':
            print("Oops, None is not a command")
            continue
        command, *args = request.split()

        if command == 'upload':
            try:
                filename = args[0]
                with open(os.path.join(os.getcwd(), filename), 'r') as f:
                    content = f.read()
                sock.send((command+" "+filename+" "+content).encode())
            except:print("try again")

        elif command == 'download':
            try:
                sock.send(request.encode())
                response = sock.recv(1024).decode()
                print(response)

                filename = args[0]
                with open(os.path.join(os.getcwd(), filename), 'w') as f:
                    f.write(response)
            except:pass

        else:
            sock.send(request.encode())
            response = sock.recv(1024).decode()

            print(response)
finally:
    sock.close()