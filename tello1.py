#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

import threading 
import socket
import sys
import time
import platform  

host = ''
port = 9000
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)
sock.settimeout(10)################
RESPONSE = False

def recv():
    global RESPONSE
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            RESPONSE = data.decode(encoding="utf-8")
            #print(RESPONSE)
        except Exception:
            RESPONSE = "timeout"
            print ('------timeout')
            

def send_cmd(cmd):
    global RESPONSE
    print(cmd)
    c = cmd.encode(encoding="utf-8")
    RESPONSE = False
    sent = sock.sendto(c, tello_address)
    while not RESPONSE:
        if RESPONSE == "timeout":
            send_cmd(cmd)
        #print(RESPONSE)
    print(RESPONSE)
    
    
print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()
#tof
for c in ["command", "takeoff", "speed 20", "ccw 90", "forward 40", "back 30", "land", "temp?", "wifi?", "battery?",  "land"]:
    send_cmd(c)


#####################
while True: 
    try:
        python_version = str(platform.python_version())
        version_init_num = int(python_version.partition('.')[0]) 
       # print (version_init_num)
        if version_init_num == 3:
            msg = input("");
        elif version_init_num == 2:
            msg = raw_input("");
        
        if not msg:
            break  

        if 'end' in msg:
            print ('...')
            sock.close()  
            break

        # Send data
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break




