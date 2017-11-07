#! /usr/bin/python2
import os
import socket
import signal
import sys
import json
from ms_excel_parser import (parse_specific_info,
                             ExcelParseError)

def ctrlplusc(a,b):
    print "\nExit Server Program."
    sys.exit(1)

if __name__ == "__main__":
    ###catch keyboardinterrupt signal
    signal.signal(signal.SIGINT, ctrlplusc)
    ###
    sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sobj.setblocking(1)
    sobj.bind((server_ip, server_port))
    sobj.listen(1)
    print 'Server listening...'
    while True:
        newobj, addr = sobj.accept()
        newobj.setblocking(0) #this is a MUST
        print "client {} connection accept.".format(addr[0])
        ##write socket data to local disk
        sfd = open(local_file_path, 'wb+') #modification in your case
        r_bytes = 0
        while True:
            #newobj.setblocking(0)
            try:
                fdata = newobj.recv(4096)
                if fdata:
                    sfd.write(fdata)
                    r_bytes += len(fdata)
                    continue
            except socket.error:
                break
        sfd.close()
        ##send back data to socket client as response
        try:
            if r_bytes == 0:
                newobj.sendall(json.dumps({'warning': 'No any data sent from web server'}))
            else:
                res = parse_specific_info(local_file_path, 0)
                newobj.sendall(json.dumps({'data': res}))
        except IOError:
            etype, eval = sys.exc_info()[:2] 
            newobj.sendall(json.dumps({'err': 'Failed to parse excel file,' + \
                                       ' possibly as office service down.'}))
        except ExcelParseError as e:
            newobj.sendall(json.dumps({'err': e.value}))
        finally:
            newobj.close()
            print 'client {} connection closed.'.format(addr[0])
