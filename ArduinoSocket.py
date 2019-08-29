import socket
import sys
import base64
import select
import os


dataInt = ''
serverIP = sys.argv[1:]
print('Server lisetining on: {0} port {1}'.format(serverIP[0], str(serverIP[1])))
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get the server address IP and port from the main script
server_address = (serverIP[0], int(serverIP[1]))
# Bind the socket to the port
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
try:
    while True:

        try:
            # Wait for a connection
            print('waiting for a client connection...')
            connection, client_address = sock.accept()
            print('connection from %s:%d' % client_address)
            connection.settimeout(60)
            while True:
                # Receive the data one byte at a time
                data = connection.recv(1)
                # print(data)
                # if not data == '\n':
                    # dataInt = dataInt + ''.join( c for c in data if  c not in '\rn\'' )
                dataInt = dataInt + ''.join( c for c in data.decode('ASCII') if  c not in '\n\r' )
                # else:
                # print(dataInt)
                if data:
                    # sys.stdout.write(data.decode('utf-8'))
                    with open('output1.txt', 'w') as f1:
                        # f1.write('test')
                        if data == b'\n':
                            # print(dataInt)
                            f1.write(dataInt)
                            dataInt = ''
                        # sleep(1)
                    # Send back in uppercase
                    # connection.sendall(data.upper())
        except socket.timeout as e:
            err = e.args[0]
            if err == 'timed out':
                # cmd = 'for /f "tokens=5" %a in (\'netstat -aon ^| find "65432"\') do taskkill /f /pid %a'
                # os.system(cmd)
                print ('received timed out, Client disconnected. ')
                connection.close()
                print('Opening new connection... ')
                continue

finally:
    sys.stdout.write('Server shut down')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
