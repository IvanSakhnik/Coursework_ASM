data segment
A1 dd 12h
A2 dw 117
A3 db 01001b
A4 dd 5
Text1 db "Qwerty167"
data ends 

T EQU 13
T1 EQU 0

code segment
B1 dd 10h
B2 dd 011b
dec B1
dec B2
movsd 
Point:
jbe M1
inc ebx
if T
dec byte ptr [eax+esi]
add ebx, edx
else
cmp eax, [ebx+ecx]
endif
dec A1
dec A4
and es:[ebx+ecx], ebx
jbe Point
mov eax, 13h
if T1
inc ah
else
mov al, 0h
endif
or dword ptr[eax+esi], 132h
M1:
code ends
END 

