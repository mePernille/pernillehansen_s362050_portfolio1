# a simple iPerf program
import argparse
from socket import *
import sys

def check_port(valu):
    try:
        value = int(valu)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
    if (value <= 0):
        print('a port must be above zero')
        sys.exit()
    return value        

parser = argparse.ArgumentParser(description="A simple iPerf version", epilog="end of help")

parser.add_argument('-s','--server', action='store_true')

#parser.add_argument('-l', '--values', help)
parser.add_argument('-p','--port',type=check_port)

#parser.add_argument()

args = parser.parse_args() # denne MÅ være under add_arguments


print("port number: ", args.port)
if args.server:
    print('The server is on', args.server)

'''
def server(ip,port,format): #format?
    serverPort = 8080 # skal man kunne vælge port selv?
    serverSock = socket(AF_INET,SOCK_STREAM)
    try:
        serverSock.bind(('',serverPort))
    except:
        print("Bind failed!")
        sys.exit()
    serverSock.listen()        
    '''