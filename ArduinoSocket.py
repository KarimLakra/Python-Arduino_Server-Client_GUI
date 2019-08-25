import socket
import sys
import base64
# import subprocess
# myList=sys.argv[1:]
# print(myList)

serverIP = sys.argv[1:]
print('Server lisetining on: {0} port {1}'.format(serverIP[0], str(serverIP[1])))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
# server_address = ('192.168.1.2', 65432)
server_address = (serverIP[0], int(serverIP[1]))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

try:
    while True:
        # Wait for a connection
        print('waiting for a connection...')
        connection, client_address = sock.accept()
        print('connection from %s:%d' % client_address)
        try:
            while True:
                # Receive the data one byte at a time
                data = connection.recv(1)
                # sys.stdout.write(data)
                sys.stdout.write(data.decode('utf-8'))

                if data:
                    # Send back in uppercase
                    connection.sendall(data.upper())
                    sys.stdout.write('DATA sent in UPPER')
                else:
                    # print('no more data, closing connection.')
                    # break
                    # Wait for a connection
                    print('waiting for a connection AGAIN...')
                    sys.stdout.write('waiting for a connection AGAIN...')
                    connection, client_address = sock.accept()
                    print('AGAIN connection from %s:%d' % client_address)
                    sys.stdout.write('AGAIN connection from %s:%d' % client_address)
        finally:
            # Clean up the connection
            connection.close()
except KeyboardInterrupt:
    print('exiting.')
    sys.stdout.write('exiting.')
finally:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
