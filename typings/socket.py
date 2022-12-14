"""
socket module. See: https://docs.micropython.org/en/v1.17/library/socket.html

|see_cpython_module| :mod:`python:socket` https://docs.python.org/3/library/socket.html .

This module provides access to the BSD socket interface.
"""
# MCU: {'ver': 'v1.17', 'port': 'pyboard', 'arch': 'armv7emsp', 'sysname': 'pyboard', 'release': '1.17.0', 'name': 'micropython', 'mpy': 7685, 'version': '1.17.0', 'machine': 'PYBv1.1 with STM32F405RG', 'build': '', 'nodename': 'pyboard', 'platform': 'pyboard', 'family': 'micropython'}
# Stubber: 1.5.4
from typing import Any, Optional, Tuple

AF_INET = 2  # type: int
AF_INET6 = 10  # type: int
SOCK_DGRAM = 2  # type: int
SOCK_RAW = 3  # type: int
SOCK_STREAM = 1  # type: int


def getaddrinfo(host, port, af=0, type=0, proto=0, flags=0, /) -> Any:
    """
    Translate the host/port argument into a sequence of 5-tuples that contain all the
    necessary arguments for creating a socket connected to that service. Arguments
    *af*, *type*, and *proto* (which have the same meaning as for the `socket()` function)
    can be used to filter which kind of addresses are returned. If a parameter is not
    specified or zero, all combinations of addresses can be returned (requiring
    filtering on the user side).

    The resulting list of 5-tuples has the following structure::

       (family, type, proto, canonname, sockaddr)

    The following example shows how to connect to a given url::

       s = socket.socket()
       # This assumes that if "type" is not specified, an address for
       # SOCK_STREAM will be returned, which may be not true
       s.connect(socket.getaddrinfo('www.micropython.org', 80)[0][-1])

    Recommended use of filtering params::

       s = socket.socket()
       # Guaranteed to return an address which can be connect'ed to for
       # stream operation.
       s.connect(socket.getaddrinfo('www.micropython.org', 80, 0, SOCK_STREAM)[0][-1])
    """
    ...


class socket:
    """
    Create a new socket using the given address family, socket type and
    protocol number. Note that specifying *proto* in most cases is not
    required (and not recommended, as some MicroPython ports may omit
    ``IPPROTO_*`` constants). Instead, *type* argument will select needed
    protocol automatically::

         # Create STREAM TCP socket
         socket(AF_INET, SOCK_STREAM)
         # Create DGRAM UDP socket
         socket(AF_INET, SOCK_DGRAM)
    """

    def __init__(self, af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP, /) -> None:
        """"""
        ...

    def close(self) -> Any:
        """
        Mark the socket closed and release all resources. Once that happens, all future operations
        on the socket object will fail. The remote end will receive EOF indication if
        supported by protocol.

        Sockets are automatically closed when they are garbage-collected, but it is recommended
        to `close()` them explicitly as soon you finished working with them.
        """
        ...

    def send(self, bytes) -> int:
        """
        Send data to the socket. The socket must be connected to a remote socket.
        Returns number of bytes sent, which may be smaller than the length of data
        ("short write").
        """
        ...

    def accept(self) -> Tuple:
        """
        Accept a connection. The socket must be bound to an address and listening for connections.
        The return value is a pair (conn, address) where conn is a new socket object usable to send
        and receive data on the connection, and address is the address bound to the socket on the
        other end of the connection.
        """
        ...

    def bind(self, address) -> Any:
        """
        Bind the socket to *address*. The socket must not already be bound.
        """
        ...

    def connect(self, address) -> None:
        """
        Connect to a remote socket at *address*.
        """
        ...

    def listen(self, backlog: Optional[Any] = None) -> None:
        """
        Enable a server to accept connections. If *backlog* is specified, it must be at least 0
        (if it's lower, it will be set to 0); and specifies the number of unaccepted connections
        that the system will allow before refusing new connections. If not specified, a default
        reasonable value is chosen.
        """
        ...

    def recv(self, bufsize) -> bytes:
        """
        Receive data from the socket. The return value is a bytes object representing the data
        received. The maximum amount of data to be received at once is specified by bufsize.
        """
        ...

    def recvfrom(self, bufsize) -> Tuple:
        """
        Receive data from the socket. The return value is a pair *(bytes, address)* where *bytes* is a
        bytes object representing the data received and *address* is the address of the socket sending
        the data.
        """
        ...

    def sendto(self, bytes, address) -> None:
        """
        Send data to the socket. The socket should not be connected to a remote socket, since the
        destination socket is specified by *address*.
        """
        ...

    def setblocking(self, flag) -> Any:
        """
        Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking,
        else to blocking mode.

        This method is a shorthand for certain `settimeout()` calls:

        * ``sock.setblocking(True)`` is equivalent to ``sock.settimeout(None)``
        * ``sock.setblocking(False)`` is equivalent to ``sock.settimeout(0)``
        """
        ...

    def setsockopt(self, level, optname, value) -> None:
        """
        Set the value of the given socket option. The needed symbolic constants are defined in the
        socket module (SO_* etc.). The *value* can be an integer or a bytes-like object representing
        a buffer.
        """
        ...

    def settimeout(self, value) -> Any:
        """
        **Note**: Not every port supports this method, see below.

        Set a timeout on blocking socket operations. The value argument can be a nonnegative floating
        point number expressing seconds, or None. If a non-zero value is given, subsequent socket operations
        will raise an `OSError` exception if the timeout period value has elapsed before the operation has
        completed. If zero is given, the socket is put in non-blocking mode. If None is given, the socket
        is put in blocking mode.

        Not every :term:`MicroPython port` supports this method. A more portable and
        generic solution is to use `select.poll` object. This allows to wait on
        multiple objects at the same time (and not just on sockets, but on generic
        `stream` objects which support polling). Example::

             # Instead of:
             s.settimeout(1.0)  # time in seconds
             s.read(10)  # may timeout

             # Use:
             poller = select.poll()
             poller.register(s, select.POLLIN)
             res = poller.poll(1000)  # time in milliseconds
             if not res:
                 # s is still not ready for input, i.e. operation timed out
        """
        ...
