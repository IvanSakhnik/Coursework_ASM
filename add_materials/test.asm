.386
data segment
A1 dd 12h
A2 dw 117
A3 db 01001b
Text1 db "Qwerty167"
data ends 

T EQU 13
T1 EQU 0

code segment
Assume cs:code, ds:data
B1 dd 10h
dec B1
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

