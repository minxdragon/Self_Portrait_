# Receiving/Sending from Processing
# Processing to send 'type', 'path', 'keyword,keyword,keyword'(if applicable)
import socket

HOST = ''              
PORT = 5005     
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print(f'Connected by', addr)
        while True:
            # Receiving from Processing
            data = conn.recv(1024)
            stringdata = data.decode('utf-8')
            print(f'Received | ' + stringdata)
            # Sending confirmation back to from Processing
            print(f'Sending...')
            conn.sendall(b"'type', 'path', 'keyword,keyword,keyword'")
            if not data: break