data segment
A1 dd 12h
A2 dw 117
A3 db 01001b
Text1 db "Qwerty167"
data ends 

T EQU 13
T1 EQU 0

code segment
movsd add
Point:
jbe erPoint
inc [ebx+ecx]
if T
dec ah
add ebx, [ebx+ecx]
endif
cmp [ebx+ecx], eax
and es:[ebx+ecx], 12h
jbe Point
mov eax
else
mov al, 0h
endif
or eax, 132h
M1:
code ends
END 

