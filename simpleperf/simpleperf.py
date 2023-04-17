# a simple iPerf program
import argparse
#from socket import *
import socket
import sys
import re
import time
import threading

# A helper fucntion, strongly inspired by Sadiqul github example. 
# It tests the given port number and raising a error if its not a number, or if the given number is'nt in the given range.
def check_port(valu): 
    try:
        value = int(valu) #testing the port value
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
    if (value < 1024 ): 
        print('port must be above 1024')
        
    elif(value > 65535):
        print("port must be les then 65535")    
    else:
        return value  

# A helper function thats checking the ip adress, i took some of the code from the link below.
# Here its important that the ip adress match the specifications given. 
def check_ip(addres):
    try:
        ipValue = str(addres)
    except:
        raise argparse.ArgumentError('must be different format')
    #https://www.abstractapi.com/guides/python-regex-ip-address
    match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ipValue)
    if not match:
        print("You must enter a valid Ip address")
        sys.exit() # when IP not valid the system will exit. 
    else:
        return ipValue
# helper function to test that the given number is in the given range. 
# also check if its a number.         
def time_int(num):
    num = int(num)
    try:
        num
    except ValueError:
        raise argparse.ArgumentTypeError('expected an interger!')
        
    if(num <= 0):
        print('Must be above 0')
    return num


def handleClient(connectionSocket, addr, format,ip,port): # The client takes inn five parameters. 
    received_bytes = 0 # making a variable to store bytes. 
    start_time = time.time() # starting the time
    while True:
        
        try:
            data = connectionSocket.recv(1000) # setting the server up to receive data. 
            if not data:
                break # It breaks out of the try: if there are no data
            if b'BYE' in data: # If the client is done and sending bye, the server will then send the ack bye back.
                connectionSocket.send(b'ACK:BYE')
            received_bytes += len(data) # Counting how many packets reseived
           
        except:
            print("something went wrong with the message") 
            connectionSocket.close() # if something is wrong with the data packet, the socket will close the connection
        end_time = time.time()    # stopping the time
        interval = end_time - start_time  # calculating  the time spend resieving data. 
        
        #under here the recieved_bytes is beeing calculatede into the desiraed format.  
        if format == 'B':
                r_bytes = received_bytes
        elif format == 'KB':
                r_bytes = received_bytes / 1000
        elif format == 'MB':
                r_bytes = received_bytes / (1000 * 1000) 

        rate = (received_bytes * 8)/(interval*1000000) # calculating the rate. 

        # under I used the build in python functionality .format() to print out my reault in a table looking way. 

    print('{:<20} | {:<15} | {:<15} | {:<15}'.format('ID', 'Interval', 'Received', 'Rate'))
    print('--------------------------------------------------------------------------')
    print('{:<20} | {:<15} | {:<15} | {:<15}'.format(str(ip)+':'+str(port), '{:.2f}'.format(interval), str(int(r_bytes)) + ' ' + format, '{:.2f}'.format(rate) + ' Mbps'))



def server(ip, port, serverip, format): # The server takes in the parameters from args.parser
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a server socket object
    try:
        serverSocket.bind((ip, port)) # binding the ip and port to the socket.
    except: # if the bind operation fails, the program will print an error and exiting the systemt. 
        print("bind fail!")
        sys.exit()
    serverSocket.listen(5) # The server start to listen for incomming clients.
    print('---------------------------------------------')
    print(f'A simpleperf server is listening on port {port}')
    print('---------------------------------------------\n')

    # below the server is accepting incomming client, i made a thread becauce I had the parallel falg in mind ( which i did not make)
    while True:
        connectionSocket, addr = serverSocket.accept() 
        thread = threading.Thread(target=handleClient, args=(connectionSocket, addr,format,ip,port)) # Sending all the necessary arguments to the handleclient
        thread.start()
        print(f'A simpleperf client with <{ip}:{port}> is connected with <{serverip}:{port}>\n')
    
    connectionSocket.close()    


def client(serverip, port, max_time, f): # taking in al the necessary arguments
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a new socket object
    serverAddr = (serverip, port )
    try:
        clientSocket.connect(serverAddr) # trying to connect to server, and printing if it goes well
        print('----------------------------------------------------------------')
        print(f'A simpleperf client connecting to server <{serverip}>, port {port}')
        print('----------------------------------------------------------------\n')
    except ConnectionError as e:
        print(e) # catching and printing any error. 
        print("Something went wrong! Did not connect client to server")
        sys.exit()
    packet_count = 0 # creating a variable to keep track of the packet count
    while True: # while the client is active:
        
        try:
            packet = b'0'*1000 # with the b in the front the packet is automatic made into bytes. 
            t = time.time() + max_time 
            while time.time() < t: # The client will send packets off 1000 * '0' while the time is less then default 25 sec, or a chosen number
                clientSocket.send(packet) # the packet is sent
                packet_count += 1 # counting 

            # calculating the correct number for a given format:
            if f == 'B':
                send_bytes = packet_count * 1000
            elif f == 'KB':
                send_bytes = packet_count
            elif f == 'MB':
                send_bytes = packet_count / 1000

            bandwidth = ((packet_count*1000) * 8)/(max_time*1000000)   # calculating the bandwidth to print:

            print('{:<20} | {:<15} | {:<15} | {:<15}'.format('ID', 'Interval', 'Transfer', 'Bandwidth'))
            print('------------------------------------------------------------------------------')
            print('{:<20} | {:<15.2f} | {:<15} | {:<10.2f}'.format(str(serverip)+':'+str(port), max_time, str(int(send_bytes))+' '+str(f), float(bandwidth))+' Mbps')


            clientSocket.send(b'BYE') # When the client is done sending bytes it will send bye
            clientSocket.recv(1000) # to recive the ack bye
            break
              
        except KeyboardInterrupt:
            print(" BYE")
            break

    clientSocket.close()

def main():

    # setting up the arg parser to recieve input from the user and sending it to the client and server 
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
    parser.add_argument('-i', '--interval', type=int) # not implementet
    parser.add_argument('-P', '--parallel', type=int, default=1) # nm: not implementet
    parser.add_argument('-n', '--num', type=str, choices=['B', 'KB', 'MB'])# not implementet
    
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

