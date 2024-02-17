# PYTHON REVERSE SHELL

so, this is pretty easy, change the ips and ports in the client.py and server.py to your ip and free port.

if the client executes it you should have access to his console.


## special commands
- !download <filename> - download a file
- !upload <filename> - upload a file
- !type <string> - type something on his simulated keyboard (like this: "!type test1<|><enter><|>test2")
- !payload <filename> - enter filename of the payload and execute it.
- !remove <filename> - remove a file/folder


## payload construction
- HOTKEY <hotkey> - enter a hotkey (e.g.: HOTKEY win+r)
- SLEEP <seconds> - sleep for a set amount
- STRING <string> - just types something
- PRESS <key> - presses a key (e.g.: PRESS enter)
- MOVEMOUSE <x+y> - moves the mouse to set x and y coords (e.g.: MOVEMOUSE 100+200)
- LMB <number> - left clicks for a set amount (e.g.: LMB 3 - clicks 3 times)
- RMB <number> - right clicks for a set amount (e.g.: RMB 3 - clicks 3 times)
- MMB <number> - middle clicks for a set amount (e.g.: MMB 3 - clicks 3 times)
- SCROLL <number> - scroll for a set amount of "clicks" (e.g.: SCROLL 20 - scrolls 20 times)

feel free to suggest even more!

