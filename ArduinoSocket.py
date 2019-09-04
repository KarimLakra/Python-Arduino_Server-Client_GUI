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
        def initCom():
            def iniAll(f):
                f = open(f, "w").close()    # clear data buffer init

            # iniAll("output.txt")    # clear server events
            iniAll("output1.txt")   # clear data buffer
            iniAll("com")           # clear server-client feedback file

        try:
            f = open("com", "w")
            f.write("Wait")
            f.close()    # set com to True, for ready to read data
            # Wait for a connection
            print('waiting for a client connection...')
            connection, client_address = sock.accept()
            print('connection from %s:%d' % client_address)
            connection.settimeout(30)   # reset the connection to client if no data is received after 60s
            while True:
                # Receive the data one byte at a time
                data = connection.recv(1)
                dataInt = dataInt + ''.join( c for c in data.decode('ASCII') if  c not in '\n\r' )
                if data:
                    # sys.stdout.write(data.decode('utf-8'))
                    with open('output1.txt', 'w') as f1:
                        if data == b'\n':
                            # print(dataInt)
                            f1.write(dataInt)
                            dataInt = ''
                            f = open("com", "w")
                            f.write("True")
                            f.close()    # set com to True, for ready to read data

                    # Send back in uppercase
                    # connection.sendall(data.upper())
        except socket.timeout as e:
            err = e.args[0]
            if err == 'timed out':
                print ('received timed out, Client disconnected. ')
                initCom()
                connection.close()
                print('Opening new connection... ')
                continue

finally:
    sys.stdout.write('Server shut down')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
