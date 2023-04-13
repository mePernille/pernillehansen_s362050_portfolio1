# a simple iPerf program
import argparse
#from socket import *
import socket
import sys
import re
import time
import threading

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


def handleClient(connectionSocket, addr, format,ip,port): 
    received_bytes = 0
    start_time = time.time()
    while True:
        
        try:
            data = connectionSocket.recv(1000)
            if not data:
                break
            received_bytes += len(data) # Counting how many packets reseived
           
        except:
            print("something went wrong with the message")
            connectionSocket.close()
        end_time = time.time()    
        interval = end_time - start_time  
        
        if format == 'B':
                r_bytes = received_bytes
        elif format == 'KB':
                r_bytes = received_bytes / 1000
        elif format == 'MB':
                r_bytes = received_bytes / (1000 * 1000) 
    print('{:<20} | {:<15} | {:<15} | {:<15}'.format('ID', 'Interval', 'Received', 'Rate'))
    print('--------------------------------------------------------------------------')
    print('{:<20} | {:<15} | {:<15} | {:<15}'.format(str(ip)+':'+str(port), '{:.2f}'.format(interval), '{:.3f}'.format(r_bytes) + ' ' + format, 'y Mbps'))

    
    connectionSocket.send(b'ACK')
    #connectionSocket.close()

def server(ip, port, serverip, format): # må sende format til handleclient på en måde
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind((ip, port))
    except:
        print("bind fail!")
        sys.exit()
    serverSocket.listen(5)
    print('---------------------------------------------')
    print(f'A simpleperf server is listening on port {port}')
    print('---------------------------------------------\n')

    while True:
        connectionSocket, addr = serverSocket.accept()
        thread = threading.Thread(target=handleClient, args=(connectionSocket, addr,format,ip,port)) # ekstra komma på slutten
        thread.start()
        print(f'A simpleperf client with <{ip}:{port}> is connected with <{serverip}:{port}>\n')
    
    connectionSocket.close()    


def client(serverip, port, max_time, f):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (serverip, port )
    try:
        clientSocket.connect(serverAddr)
        print('----------------------------------------------------------------')
        print(f'A simpleperf client connecting to server <{serverip}>, port {port}')
        print('----------------------------------------------------------------\n')
    except ConnectionError as e:
        print(e)
        print("Something went wrong! Did not connect client to server")
        sys.exit()
    packet_count = 0
    while True:
        
        try:
            packet = b'0'*1000 # with the b in the front the packet is automatic made into bytes. 
            t = time.time() + max_time 
            while time.time() < t: # The client will send packets off 1000 * '0' while the time is less then default 25 sec, or a chosen number
                clientSocket.send(packet) # the packet is sent
                packet_count += 1

            if f == 'B':
                send_bytes = packet_count * 1000
            elif f == 'KB':
                send_bytes = packet_count
            elif f == 'MB':
                send_bytes = packet_count / 1000

            print('{:<20} | {:<15} | {:<15} | {:<15}'.format('ID', 'Interval', 'Transfer', 'Bandwidth'))
            print('------------------------------------------------------------------------------')
            print('{:<20} | {:<15.2f} | {:<15} | {:<15}'.format(str(serverip)+':'+str(port), max_time, str(send_bytes)+' '+f, 'hej'))

            print('Bye') # When the client is done sending bytes it will print bye
            break   
        except KeyboardInterrupt:
            print(" BYE")
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
    parser.add_argument('-i', '--interval', type=int)
    parser.add_argument('-P', '--parallel', type=int, default=1)
    parser.add_argument('-n', '--num', type=str, choices=['B', 'KB', 'MB'])
    
    args = parser.parse_args() 
    
    
    if args.server and args.client:
        print("You must run either the server OR the client")
        sys.exit()

    if args.server:
        server(args.bind , args.port , args.serverip, args.format) #sending the two arguments to the server def

    if args.client:
        client(args.serverip, args.port, args.time, args.format)# and sending to the clint def.
        


if __name__ == '__main__':
    main()        

