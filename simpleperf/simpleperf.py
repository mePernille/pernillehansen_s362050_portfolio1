# a simple iPerf program
import argparse
from socket import *
import sys
import re
import time
import _thread as thread

allClients = [] # an array to keep all the clients in

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
        
def time_int(num):
    
    try:
        num
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
        
    if(num <= 0):
        print('Must be above 0')
    return num


def handleClient(connectionSocket, addr): #DENNE def er jeg i tvivl om jeg må ha med!
    allClients.append(connectionSocket)
    
    # NÅR skal den lukkes?
    connectionSocket.close()
    allClients.remove(connectionSocket)

def server(ip, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind((ip, port))
    except:
        print("bind fail!")
        sys.exit()
    serverSocket.listen(5)
    print('---------------------------------------------')
    print(f'A simpleperf server is listening on port {port}')
    print('---------------------------------------------')

    while True:
        connectionSocket, addr = serverSocket.accept() # HVORFOR er denne addr ikke brugt??
        thread.start_new_thread(handleClient, (connectionSocket, addr,))
        try:
            message = connectionSocket.recv(1000).decode()
            print(message)
            
        except:
            print("something wrong with the message")
            connectionSocket.close()    


def client(serverip, port, max_time):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    serverAddr = (serverip, port )

    try:
        clientSocket.connect(serverAddr)
    except ConnectionError:
        print("Something went wrong! Did not connect client to server")

    while True:
        try:
         packet = '0'*1000
         t = time.time() + max_time
         while t < max_time:
            for p in packet:
                 clientSocket.send(packet.encode())
                 # reply = clientSocket.recv(2048).decode() Sfiqul sagde denne ikke skulle være med
        except KeyboardInterrupt:
            print("BYE") # DENNE printes ikke ud
          #  clientSocket.close()
          #  break
            # return reply , denne vil bare retunerer alle 0'erne. det er ikke det jeg skal returnere        
        clientSocket.close()

def main():

    parser = argparse.ArgumentParser(description="A simple iPerf version", epilog="end of help")

    parser.add_argument('-s','--server', action='store_true')
    parser.add_argument('-b', '--bind', type=check_ip, default='127.0.0.1')
    parser.add_argument('-p','--port',type=check_port, default=8088)
    parser.add_argument('-f', '--format', type=str, )# denne må gjøres        
    
    parser.add_argument('-c', '--client', action='store_true')
    parser.add_argument('-I', '--serverip', type=check_ip, default='127.0.0.1')
    parser.add_argument('-t', '--time', type=time_int, default=25)
    parser.add_argument('-i', '--interval', type=int, )
    
    args = parser.parse_args() # denne MÅ være under add_arguments
    # 1MB = 1000 KB, 1KB = 1000 Bytes 
    
    if args.server and args.client:
        print("You must rund either the server OR the client")
        sys.exit()

    if args.server:
        server(args.bind , args.port) #sending the two arguments to the server def

    if args.client:
        client(args.serverip, args.port, args.time)# and sending to the clint def.
        


if __name__ == '__main__':
    main()        


'''
# sån lager man 1000 bites
x = '0' * 1000
print(x)
'''