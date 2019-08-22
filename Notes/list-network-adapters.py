import sys
import netifaces

# ad = netifaces.interfaces()
# print(ad)

def listAddrs():
    ad = netifaces.interfaces()
    for adpt in ad:
        # print(netifaces.ifaddresses(adpt))
        va = netifaces.ifaddresses(adpt)
        if 2 in va:
            print(netifaces.ifaddresses(adpt)[2][0]['addr'])

listAddrs()
