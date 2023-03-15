# a simple iPerf program
import argparse
from socket import *
import sys

parser = argparse.ArgumentParser(description="positional arguments", epilog="end of help")

# her skal være parser.add_argument('name', )
parser.add_argument('-s','--server', action='store_true')
parser.add_argument()
parser.add_argument()
parser.add_argument()

args = parser.parse_args() # denne MÅ være under add_arguments

#if args.server:
#    print('The server is on', args.server)


def server(ip,port,format): #format?
    serverPort = 8080 # skal man kunne vælge port selv?
    serverSock = socket(AF_INET,SOCK_STREAM)
    try:
        serverSock.bind(('',serverPort))
    except:
        print("Bind failed!")
        sys.exit()    