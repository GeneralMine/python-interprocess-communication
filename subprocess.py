#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Python2 using Python3 Subprocess

import os
import subprocess
import sys

def version():
    return '.'.join('%d' % e for e in sys.version_info[0:3])


def server():
    r, w = os.pipe()
    process = subprocess.Popen(['python3', sys.argv[0],
                                '%d' % r, '%d' % w],
                                close_fds=False)
    os.close(w)
    msg = os.read(r, 100)
    print("From Python %s: %s" % (version(), msg))
    os.close(r)


def client(r, w):
    os.close(r)
    msg = "Hello from Python %s" % version()
    msg = msg.encode('utf-8')
    os.write(w, msg)
    os.close(w)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        server()
    else:
        client(int(sys.argv[1]), int(sys.argv[2]))