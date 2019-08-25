import sys
import socket
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.2',65432))
s.settimeout(2)

while True:
    try:
        msg = s.recv(4096)
    except socket.timeout as e:
        err = e.args[0]
        # this next if/else is a bit redundant, but illustrates how the
        # timeout exception is setup
        if err == 'timed out':
            sleep(1)
            print ('recv timed out, retry later')
            continue
        else:
            print (e)
            sys.exit(1)
    except socket.error as e:
        # Something else happened, handle error, exit, etc.
        print (e)
        sys.exit(1)
    else:
        if len(msg) == 0:
            print ('orderly shutdown on server end')
            sys.exit(0)
        else:
            # got a message do something :)
            print('NO')
