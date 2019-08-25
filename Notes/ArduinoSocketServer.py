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
# server_address = ('', int(serverIP[1]))
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
                # sys.stdout.write(data.decode('utf-8'))
                sys.stdout.write('.')

                try:
                    if data:
                        # Send back in uppercase
                        connection.sendall(data.upper())
                    else:
                        print('no more data, closing connection.')
                        sys.stdout.write('no more data, closing connection.')
                        break
                except socket.error:
                    # client.remove(sock)
                    sys.stdout.write('Client removed')
        finally:
            # Clean up the connection
            sys.stdout.write('connection closed')
            connection.close()

except KeyboardInterrupt:
    print('exiting.')
    sys.stdout.write('exiting.')
finally:
    sys.stdout.write('shut down')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
