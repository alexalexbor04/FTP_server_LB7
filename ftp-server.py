import socket
import os
import shutil
import datetime

HOST = '127.0.0.1'
PORT = 12345

WORKING_DIRECTORY = "rootfolder"

AUTHORIZED_USERS = {'user': '111', 'user2': '222'}

def authenticate(conn):
    #conn.send(.encode())
    login = conn.recv(1024).decode()
    conn.send("Введите пароль: ".encode())
    password = conn.recv(1024).decode().strip()

    if login in AUTHORIZED_USERS and AUTHORIZED_USERS[login] == password:
        conn.send("Авторизация успешна".encode())
        return True
    else:
        conn.send("Неверный логин или пароль. Соединение разорвано.".encode())
        return False

def log_action(action, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{action}_log.txt", "a") as logfile:
        logfile.write(f"[{timestamp}] {message}\n")

def process(request):

    print(request)
    command, *args = request.split()

    if command == 'pwd':
        return WORKING_DIRECTORY
    elif command == 'ls':
        return '  '.join(os.listdir(WORKING_DIRECTORY))
    elif command == 'mkdir':
        os.mkdir(os.path.join(WORKING_DIRECTORY, args[0]))
        return f"Папка {args[0]} создана"
    elif command == 'rmdir':
        shutil.rmtree(os.path.join(WORKING_DIRECTORY, args[0]))
        return f"Папка {args[0]} удалена"
    elif command == 'rm':
        os.remove(os.path.join(WORKING_DIRECTORY, args[0]))
        return f"Файл {args[0]} удален"
    elif command == 'rename':
        os.rename(os.path.join(WORKING_DIRECTORY, args[0]), os.path.join(WORKING_DIRECTORY, args[1]))
        return f"Файл {args[0]} переименован в {args[1]}"
    elif command == 'upload':
        try:
            filename = args[0]
            content = args[1]
            with open(os.path.join(WORKING_DIRECTORY, filename), 'w') as f:
                f.write(content)
            return f"Файл {filename} загружен на сервер"
        except:pass
    elif command == 'download':
        try:
            filename = args[0]
            with open(os.path.join(WORKING_DIRECTORY, filename), 'r') as f:
                content = f.read()
            return content
        except:pass
    elif command == 'exit':
        return "Выход из программы"
    else:
        return 'Неверный запрос'

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen()

while True:
    print("Слушаем порт", PORT)
    conn, addr = sock.accept()
    print(addr)

    if authenticate(conn):
        log_action("connection", f"Connection established from {addr}")

        while True:

            request = conn.recv(1024).decode()
            log_action("request", f"Request from {addr}: {request}")

            # if not request:
            #     break

            try:
                response = process(request)
                conn.send(response.encode())
                log_action("response", f"Response to {addr}: {response}")
            except:conn.send("try again".encode())

    conn.close()
sock.close()
