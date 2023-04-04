# a simple iPerf program
import argparse
from socket import *
import sys
import re
import time
import threading

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
    else:
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
    num = int(num)
    try:
        num
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
        
    if(num <= 0):
        print('Must be above 0')
    return num


def handleClient(connectionSocket, addr): 
    allClients.append(connectionSocket)
    received_bytes = 0
    while True:
        try:
            message = connectionSocket.recv(1000).decode()
            if message:
                received_bytes += 1 # Counting how many packets reseived, MUST BE made in to bytes
        except:
            print("something wrong with the message")
            break
    print(received_bytes)
    connectionSocket.close()
    allClients.remove(connectionSocket)

def server(ip, port, serverip):
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
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=handleClient, args=(connectionSocket, addr,)) # usikker på om der skal være det ekstra komma på slutten
        thread.start()
        # thread.start_new_thread(handleClient, (connectionSocket, addr,))
        print(f'A simpleperf client with <{ip}:{port}> is connected with <{serverip}:{port}>')
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
         while time.time() < t: # The client will send packets off 1000 * '0' while the time is less then default 25 sec, or a chosen number
            clientSocket.send(packet.encode())
        except KeyboardInterrupt:
            print("BYE") # DENNE printes ikke ud
          #  clientSocket.close()
            break
    clientSocket.close()

def main():

    parser = argparse.ArgumentParser(description="A simple iPerf version", epilog="end of help")

    # below is the server options listet
    parser.add_argument('-s','--server', action='store_true')
    parser.add_argument('-b', '--bind', type=check_ip, default='127.0.0.1')
    parser.add_argument('-p','--port',type=check_port, default=8088)
    parser.add_argument('-f', '--format', type=str, choices=['B', 'KB', 'MB'], default= 'MB' )        
    
    # below is the clien options listet
    parser.add_argument('-c', '--client', action='store_true')
    parser.add_argument('-I', '--serverip', type=check_ip, default='127.0.0.1')
    parser.add_argument('-t', '--time', type=time_int, default=25)
    parser.add_argument('-i', '--interval', type=int, )
    
    args = parser.parse_args() 
    
    
    if args.server and args.client:
        print("You must run either the server OR the client")
        sys.exit()

    if args.server:
        server(args.bind , args.port , args.serverip) #sending the two arguments to the server def

    if args.client:
        client(args.serverip, args.port, args.time)# and sending to the clint def.
        


if __name__ == '__main__':
    main()        

