# a simple iPerf program
import argparse
from socket import *
import sys
import re

def check_port(valu): # Taget fra safiqul sin git kode
    try:
        value = int(valu)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
    if (value < 1024 | value > 65535):
        print('a port must be between 1024 and 65535')
        sys.exit()
    return value  

def check_ip(addres):
    try:
        ipValue = str(addres)
    except:
        raise argparse.ArgumentError('must be different format')
    #https://www.abstractapi.com/guides/python-regex-ip-address
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ipValue)
    if match:
        return ipValue
    else:
        print("You must enter a valid Ip address")
        sys.exit()

    '''
    if(match not True):
        print("fejlmelding")
        sys.exit()
    return ipValue      
    '''

def server(ip, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind((ip, port))
    except:
        print("bind fail!")
        sys.exit()
    serverSocket.listen(10)
    print('Server is listening...')
    while True:
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1000).decode()
            print(message)
            
        except:
            print("something wrong with the message")
            connectionSocket.close()    

def main():

    parser = argparse.ArgumentParser(description="A simple iPerf version", epilog="end of help")

    parser.add_argument('-s','--server', action='store_true')
    #parser.add_argument('-l', '--values', help)
    parser.add_argument('-p','--port',type=check_port, default=8088)
    parser.add_argument('-b', '--bind', type=check_ip, default='localhost')
    #parser.add_argument()    
    args = parser.parse_args() # denne MÅ være under add_arguments

    '''
    søk opp python regx til at få en rigtig ip adresse.
    
    '''
    print("port number: ", args.port)
    if args.server:
        server(args.bind , args.port)
        


if __name__ == '__main__':
    main()        


'''
# sån lager man 1000 bites
x = '0' * 1000
print(x)
'''