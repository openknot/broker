"""Utilities"""


from time import sleep
from socket import AF_INET, SOCK_STREAM, socket


def parse_bind(s, default_port=1338):
    # XXX: We ignore the protocol for now
    if "://" in s:
        _, s = s.split("://", 1)

    if ":" in s:
        address, port = s.split(":", 1)
        port = int(port)
    else:
        address, port = s, default_port

    return address, port


def waitfor(address, port, timeout=10):
    sock = socket(AF_INET, SOCK_STREAM)
    counter = timeout
    while not sock.connect_ex((address, port)) == 0 and counter:
        sleep(1)
        counter -= 1
    return counter
