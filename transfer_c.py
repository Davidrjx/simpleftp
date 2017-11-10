#! /usr/local/bin/python2.7

import socket
from sendfile import sendfile
#__all__ = ['transfer_file_stream', 'traditional_transfer_file_stream']

class SocketTransportError(Exception):
    def __init__(self, value):
        self.value = value

def socketcliexc(f):
    """decorator for socket transfer client"""
    def decwrapper(fd):
        try:
            return f(fd)
        except Exception:
            raise SocketTransportError('Error from file transport ' + \
                  'server&client, possibly as file service down.')
    return decwrapper


@socketcliexc
def transfer_file_stream(fd):
    """
    send_file system call with high performance
    only applicable to regular or Django's TemporaryUploadedFile object
    """
    cliobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliobj.connect((server_ip, server_port))
    blks = fd.size
    offset = 0
    res = ''
    while True:
        ss = sendfile(cliobj.fileno(), fd.fileno(), offset, blks)
        if ss == 0:
            while True:
                tmp_res = cliobj.recv(4096*2)
                if not tmp_res: break
                res += tmp_res
            break
        offset += ss
    cliobj.close()
    return res


@socketcliexc
def traditional_transfer_file_stream(fd):
    """
    traditional socket send/sendall, worse than send_file
    """
    cliobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliobj.connect((server_ip, server_port))
    cliobj.sendall(fd.read())
    res = ''
    while True:
        tmp_res = cliobj.recv(4096*2)
        if not tmp_res: break
        res += tmp_res
    cliobj.close()
    return res
