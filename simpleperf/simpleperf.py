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
    if (value < 1024 ):
        print('port must be above 1024')
        
    elif(value > 65535):
        print("port must be les then 65535")    
    return value  

def check_ip(addres):
    try:
        ipValue = str(addres)
    except:
        raise argparse.ArgumentError('must be different format')
    #https://www.abstractapi.com/guides/python-regex-ip-address
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ipValue)
    if not match:
        print("You must enter a valid Ip address")
        sys.exit()
    else:
        return ipValue
        


def server(ip, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind((ip, port))
    except:
        print("bind fail!")
        sys.exit()
    serverSocket.listen(10)
    print('---------------------------------------------')
    print(f'A simpleperf server is listening on port {port}')
    print('---------------------------------------------')

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
    parser.add_argument('-p','--port',type=check_port, default=8088)
    parser.add_argument('-b', '--bind', type=check_ip, default='127.0.0.1')
    parser.add_argument('-f', '--format', type=str, )# denne må gjøres    
    args = parser.parse_args() # denne MÅ være under add_arguments

    
    if args.server:
        server(args.bind , args.port)
        


if __name__ == '__main__':
    main()        


'''
# sån lager man 1000 bites
x = '0' * 1000
print(x)
'''