#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import struct
try:
    import usocket as socket
except ImportError:
    import socket
import websocket_helper

# Define to 1 to use builtin "websocket" module of MicroPython
USE_BUILTIN_WEBSOCKET = 0
# Treat this remote directory as a root for file transfers
DEBUG = 0

def debugmsg(msg):
    if DEBUG:
        print(msg)


if USE_BUILTIN_WEBSOCKET:
    from websocket import websocket
else:
    class websocket:

        def __init__(self, s):
            self.s = s
            self.buf = b""

        def writeText(self, data):
            l = len(data)
            if l < 126:
                # TODO: hardcoded "binary" type
                hdr = struct.pack(">BB", 0x81, l)
            else:
                hdr = struct.pack(">BBH", 0x81, 126, l)
            self.s.send(hdr)
            self.s.send(data)

        def write(self, data):
            l = len(data)
            if l < 126:
                # TODO: hardcoded "binary" type
                hdr = struct.pack(">BB", 0x82, l)
            else:
                hdr = struct.pack(">BBH", 0x82, 126, l)
            self.s.send(hdr)
            self.s.send(data)

        def recv(self, sz):
            res = b""
            while sz:
                data = self.s.recv(sz)
                if not data:
                    break
                res += data
                sz -= len(data)
            return res

        def recvexactly(self, sz):
            res = b""
            while sz:
                data = self.s.recv(sz)
                if not data:
                    break
                res += data
                sz -= len(data)
            return res

        def readText(self):
            buff = b""
            while True:
                hdr = self.recvexactly(2)
                assert len(hdr) == 2
                fl, sz = struct.unpack(">BB", hdr)
                if sz == 126:
                    hdr = self.recvexactly(2)
                    assert len(hdr) == 2
                    (sz,) = struct.unpack(">H", hdr)
                if fl == 0x82 or fl == 0x81:
                    break
                debugmsg("Got unexpected websocket record of type %x, skipping it" % fl)
                while sz:
                    skip = self.s.recv(sz)
                    debugmsg("Skip data: %s" % skip)
                    sz -= len(skip)
            data = self.recvexactly(sz)
            assert len(data) == sz
            return data

        def read(self, size, text_ok=False):
            if not self.buf:
                while True:
                    hdr = self.recvexactly(2)
                    assert len(hdr) == 2
                    fl, sz = struct.unpack(">BB", hdr)
                    if sz == 126:
                        hdr = self.recvexactly(2)
                        assert len(hdr) == 2
                        (sz,) = struct.unpack(">H", hdr)
                    if fl == 0x82:
                        break
                    if text_ok and fl == 0x81:
                        break
                    debugmsg("Got unexpected websocket record of type %x, skipping it" % fl)
                    while sz:
                        skip = self.s.recv(sz)
                        debugmsg("Skip data: %s" % skip)
                        sz -= len(skip)
                data = self.recvexactly(sz)
                assert len(data) == sz
                self.buf = data

            d = self.buf[:size]
            self.buf = self.buf[size:]
            assert len(d) == size, len(d)
            return d

def login(ws, passwd):
    while True:
        c = ws.read(1, text_ok=True)
        if c == b":":
            assert ws.read(1, text_ok=True) == b" "
            break
    ws.write(passwd.encode("utf-8") + b"\r")

def read_resp(ws):
    resp = b''
    while resp[-3:]!=">>>":
       resp += ws.readText()
    return resp

def send_cmd(ws, cmd):
    ws.writeText(cmd.encode("utf-8") + b"\r\n")
    return read_resp(ws)    


def error(msg):
    print(msg)
    sys.exit(1)

def parse_remote(remote):
    host, fname = remote.rsplit(":", 1)
    if fname == "":
        fname = "/"
    port = 8266
    if ":" in host:
        host, port = host.split(":")
        port = int(port)
    return (host, port, fname)

def init(host, port, passwd):
    s = socket.socket()
    ai = socket.getaddrinfo(host, port)
    addr = ai[0][4]
    s.connect(addr)
    websocket_helper.client_handshake(s)
    ws = websocket(s)
    login(ws, passwd)
    return ws


if __name__ == "__main__":

    ws = init("192.168.4.1", "8266", "ofek")

    ans = send_cmd( ws, "import robot as r");    print( ans )
    ans = send_cmd( ws, "dir()");    print( ans )
    ans = send_cmd( ws, "r.pwmLeft.value(1)");    print( ans )
    ans = send_cmd( ws, "r.pwmRight.value(1)");    print( ans )
    ans = send_cmd( ws, "r.pwmLeft.value(0)");    print( ans )
    ans = send_cmd( ws, "r.pwmRight.value(0)");    print( ans )
    ans = send_cmd( ws, "dir()");    print( ans )
    
