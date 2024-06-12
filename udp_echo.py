#!/usr/bin/env python3

import socket
from argparse import ArgumentParser  # Use `import` for modules
from socket import AF_INET, SOCK_DGRAM

ECHO_PORT = 6100
BUFSIZE = 1024

if __name__ == "__main__":

  # Parse arguments
  parser = ArgumentParser()  # Correct syntax

  # Allow Controller modification and debug level sets.
  binding_group = parser.add_argument_group('Binding', 'These options change how traffic is bound.')
  binding_group.add_argument("--ip", help="IP to listen on. (Default ALL)",
                             type=str, default="0.0.0.0")
  binding_group.add_argument("--port", help="Port to listen on. (Default is 6100)", type=int,
                             default=6100)

  args = parser.parse_args()

  # Create a UDP socket
  s = socket(AF_INET, SOCK_DGRAM)

  # Bind the socket to the specified IP and port
  s.bind((args.ip, args.port))

  print('UDP echo server listening on {}:{}'.format(s.getsockname()[0], s.getsockname()[1]))

  while True:
    # Receive data from a client
    data, addr = s.recvfrom(BUFSIZE)

    # Echo the data back to the client
    s.sendto(data, addr)
