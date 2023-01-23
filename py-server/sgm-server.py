# Receiving/Sending from Processing
# Processing to send 'type', 'path', 'keyword,keyword,keyword'(if applicable)
import socket
import imgbbpy
import time
testMode = False

HOST = ''              
PORT = 5008
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print(f'Connected by', addr)
        while True:
            # Receiving from Processing
            data = conn.recv(1024)
            if not data:
                break
            stringdata = data.decode('utf-8')
            print(f'Received | ' + stringdata)

            splitMessage = stringdata.split(',')

            # face or userSelected
            if splitMessage[0] == 'cameraNoMask':
                print(f'Removed any existing masks')
                print(f'Sending...')
                conn.sendall(b"cameraNoMaskReady")
            elif splitMessage[0] == 'faceCaptured':
                # Receives face image and uploads file to imgbb
                client = imgbbpy.SyncClient('f3bab68417be3af86d5abb25a77fec64')
                if testMode == False:
                    face = client.upload(file='/Users/sgm_tech/Documents/sp-interactive/interactive/data/face.jpg', expiration=600)
                else: 
                    face = client.upload(file='/Users/melhuang/Documents/Clients/Science Gallery/Self Portrait/sp-interactive/interactive/data/face.jpg', expiration=600)
                print(face.url)
                # When prompt is ready, send back to Processing
                print(f'Sending...')
                conn.sendall(b"analysisComplete,musical&level-headed&visionary&risk-taker&creative")
                print(f'Analysis complete. Mask and Keywords sent.')
            elif splitMessage[0] == 'userSelected':
                print(f'Fetching mask...')  
                time.sleep(4)
                print(f'Sending...')                
                conn.sendall(b"cameraMaskReady,window frame name")
                print(f'Analysis complete. Mask and Keywords sent.')
            else:
                print(f'Message type not identified')

