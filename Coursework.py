#Coursework made by Ivan Sakhnik
import re,string

#ініціалізація структур для роботи з лексемами
Registers_32=('eax','ebx','edx','ecx','esi','ebp','esp','edi')                                                  #32-ох розрядні регістри
Registers_8=('ah','al','bh','bl','dh','dl','ch','cl')                                                           #8-ми розрядні регістри
Segment_Reg=('cs','ds','es','fs','gs','ss')                                                                     #сегментні регістри
Command=('movsd','inc','dec','add','cmp','and','mov','or','jbe')                                                #команди
Directive=('segment','equ','ends','end','db','dw','dd','if','else','endif')                                     #директиви
TypeOperator=('ptr',)                                                                                           #тип оператора
Number=('0','1','2','3','4','5','6','7','8','9')                                                                #десяткові числа
Number_16=('a','b','c','d','e','f','h')                                                                         #16-теричні числа
Binary=('0','1')                                                                                                #двійкові числа
SingleSymbol=('+','*',':','[',']',',')                                                                          #односимвольні лексеми
Identifier=('byte','dword')
dictionary={Registers_32:'32_bit_register', Registers_8:'8_bit_register', Segment_Reg:'segment_register',       #словник що зберігає в собі вищеописані кортежі
        Command:'command', Directive:'directive', TypeOperator:'operator_ident_type_def',
        SingleSymbol:'single_symbol', Identifier:'type_definitor'} 
EQU_list=[]                                                                                                     #список [ім'я, значення] для директиви EQU

def search_in_dictionary(lexem,_list):                                  #пошук лексеми за ключем в словнику
    if lexem in _list:
        return 1
    return 0

#Ф-ція що визначає тип лексеми    
def lexem_analyser(lexem):
    if lexem=='':
        return -1
    
    for key in dictionary:                                              #якщо лексема не є числом то шукаємо її по ключу в словнику
        if search_in_dictionary(lexem,key):
            return dictionary[key]
      
    flag=0
    if lexem[0] in Number:                                              #перевірка на те чи є лексема 16-ричним числом
        for i in range(0,len(lexem)):
            if lexem[i] in Number_16 or lexem[i] in Number:
                continue   
            else:
                flag=1
    else:
        flag=1
    if lexem[len(lexem)-1] != 'h':
        flag=1            
    if flag==0:            
        return 'hexadecimal_number'
        
    flag=0                                                              #перевірка чи є двійковим числом
    for i in range(0,len(lexem)-1):
        if lexem[i] not in Binary:
            flag=1
    if lexem[len(lexem)-1] != 'b':
        flag=1
    if flag==0:
        return 'binary_number'

    if lexem[0]=='"':                                                   #перевірка чи є текстовою константою
        if lexem[len(lexem)-1]=='"':
            return 'text_const'

    flag=0                                                              #чи є десятковим числом
    for i in range(0,len(lexem)): 
        if lexem[i] not in Number: 
            flag=1 
    if flag==0: 
        return 'decimal_number'
        
    flag=0                                                              #якщо не було знайдено лексему в словнику перевіряємо це це ідентифікатор користувача
    if len(lexem)<=8:                                                   #за умовою іденифікатори повинні бути менше 8 символів >>
        if lexem[0] in list(string.ascii_lowercase):                    #та починатися з великої або малої літери
             for i in range(1,len(lexem)):
                if lexem[i] in list(string.ascii_lowercase) or lexem[i] in Number:
                    continue
                else:
                    flag=1
        else:
            flag=1
    else:
        flag=1
                        
    if flag==1:
        return 'ERROR'
    else:
        return 'user_identifier'

# """ф-ція запису у файл результату виконання лексичного аналізатора"""        
def out_analyser(Nomber,lexem,type_lexem,file):                            
    if type_lexem==-1:
        return
    if type_lexem=='text_const':
        lexem=lexem[1:len(lexem)-1]                                     #видаляємо '"' на початку та в кінці текстової константи
    lexem=lexem.strip()                                                 #видаляє початкові і кінцеві пробіли лексеми
                                                                        #приклад ___Ivan__ >> Ivan

    """
    file.write('|%6d'%Nomber); file.write(' | %21s'%lexem); file.write(' | %11d'%len(lexem));
    file.write(' | %24s'%type_lexem); file.write('  |\n');
    file.write('-'*75); file.write('\n');
    """
    
    file.write('%d'%Nomber); file.write(' %s'%lexem); file.write(' %d'%len(lexem));
    file.write(' %s'%type_lexem); file.write('\n');

#Лексичний аналізатор    
def Analyse(filename,filename1):                                    
    analyser=open(filename1, "w");                                      #відкриття файлу для записування
    with open(filename) as test:                                        #відкриття файлу для читання

        """
        analyser.write('-'*75); analyser.write('\n')                    #запис заголовку таблиці лексичного аналізатора
        analyser.write('|%2s'%'Number'); analyser.write(' | %21s'%'Lexeme');
        analyser.write(' | %8s'%'len(lexeme)');
        analyser.write(' | %27s'%'type lexeme'' |'); analyser.write('\n')
        analyser.write('-'*75); analyser.write('\n');
        """
        
        #count=0                                                        #лічильник що рахує номер лексеми
        for line in test:
            count=0 
            line=line.split(';',1)[0]                                   #видаляємо зі строки коментарій
            line=line.lower()
            i=0
            while i < len(line):    
                if line[i] in SingleSymbol:
                    ch=line[i]
                    line=line.split(ch,1)
                    line=line[0]+' '+ch+' '+line[1]                     #розділяємо всі лексеми пробілами
                    i=i+3
                else:
                    i=i+1

            lexem=''        
            line=line.split()                                           #розбиваємо строку на список лексем
            for item in line:                                           #прохід по списку
                lexem=item
                type_lexem=lexem_analyser(lexem)                        #передаємо лексему на аналіз
                count+=1
                out_analyser(count,lexem,type_lexem,analyser)
                lexem=''
    test.close()                                                        #закриття файлів
    analyser.close()

# """ф-ція запису у файл структури речень"""
def out_struct(label,mnemocode,len_mnemo,op1,len_op1,op2,len_op2,file):
                                                                    
    file.write('|%6d'%label); file.write(' | %10d'%mnemocode); file.write(' | %10d'%len_mnemo); 
    file.write(' | %10d'%op1);  file.write(' | %10d'%len_op1);
    file.write(' | %10d'%op2);  file.write(' | %10d'%len_op2); file.write(' |\n');
    file.write('-'*87); file.write('\n');

#Структура речень    
def StructLine(filename,filename1):
    Struct=open(filename1, "w");                                        #відкриття файлу для запису структури речень
    with open(filename) as test:                                        #відкриття файлу для читання
        
        Struct.write('-'*87); Struct.write('\n')                        #запис заголовку таблиці структури речень
        Struct.write('|%6s'%'label'); Struct.write(' | %10s'%'mnemocode');
        Struct.write(' | %10s'%'LenMnemo'); Struct.write(' | %10s'%'operand_1');
        Struct.write(' | %10s'%'len_oper1'); Struct.write(' | %10s'%'operand_2');
        Struct.write(' | %10s'%'len_oper2'); Struct.write(' | \n')
        Struct.write('-'*87); Struct.write('\n');
        
        for line in test:                                               #зчитуємо строки та розбиваємо по пробілах
            if line=='' or line=='\n':
                continue
            line=line.split(';',1)[0]                       
            line=line.lower()
            i=0
            while i < len(line):    
                if line[i] in SingleSymbol:
                    ch=line[i]
                    line=line.split(ch,1)
                    line=line[0]+' '+ch+' '+line[1]                 
                    i=i+3
                else:
                    i=i+1
            lexem=''                                                    #ініціалізація циклу
            line=line.split()                                           #обнуляємо всі дані необхідні для запису структури речення
            label=0
            mnemocode=0
            len_mnemo=0
            len_op1=0
            len_op2=0
            op1=0
            op2=0
            flag=0
            count=0
            for item in line:                                           #аналізуємо окремо кожну строку
                lexem=item
                type_lexem=lexem_analyser(lexem)   
                if type_lexem=='user_identifier' and flag==0:           #заповнюємо поле label
                    count+=1
                    label=1
                    flag=1
                    lexem=''
                    continue    
                if type_lexem=='command' or type_lexem=='directive':    #заповнюємо поле mnemocode
                    count+=1
                    mnemocode=count
                    len_mnemo=1                                         #заповнюємо поле LenMnemo
                    lexem=''
                    flag=2
                    continue
                if type_lexem=='single_symbol' and flag==1:             #якщо в нас в строці лише ідентифікаор і розділовий знак
                    break                                               #то виходимо з циклу
                if lexem==',':
                    count+=1
                    flag=4
                    continue
                if lexem!=',' and flag==3:                              #рахуємо довжину операнду1 якщо >1
                    count+=1
                    len_op1+=1
                    continue
                if type_lexem!= 'command' and type_lexem!= 'directive' and flag==2:
                    count+=1
                    op1=count                                           #заповнюємо поле операнд_1
                    len_op1=1
                    flag=3
                    continue
                if op1!=0 and type_lexem!= 'command' and type_lexem!= 'directive' and flag==4:
                    count+=1
                    op2=count                                           #заповнюємо поле операнд_2
                    len_op2=1
                    flag=5
                    continue
                if op1!=0 and flag==5:
                    count+=1
                    len_op2+=1                                          #рахуємо довжину операнду2 якщо >1
                    continue

                                                                        #передаємо отримані результати в ф-цію запису у файл
            out_struct(label,mnemocode,len_mnemo,op1,len_op1,op2,len_op2,Struct)  
    test.close()                                                    
    Struct.close()

#аналіз EQU    
def analysis_equ(test_file):
    test_file=open(test_file, "r")
      
    EQU=0
    ident=0                                                                #змінна що запамятовує ідентифікатор
    value=0                                                                #змінна що запамятовує значення ідентифікатора
    
    for line in test_file:                                                 #прохід по файлу
        #line=line.lower()
        line=line.split()
        if 'EQU' in line:                                                  #якщо зустрічається EQU, запамятовуємо ідентифікатор та його значення
            ident=line[0]
            value=line[2]
            EQU_list.append(ident)                                         #отримані значення добавляємо в список
            EQU_list.append(value)
            
    test_file.close()

#ф-ція що видяляє зайві гілки програми
def delete_if_else(test, new_test):
    test=open(test, "r")
    new_test=open(new_test, "w")
    erase_flag1=0
    erase_flag2=0
    else_flag=0
    analysis_equ('test.asm')
    for line in test:
        line_copy=line
        i=0
        while i < len(line):    
                if line[i] in SingleSymbol:
                    ch=line[i]
                    line=line.split(ch,1)
                    line=line[0]+' '+ch+' '+line[1]                     
                    i=i+3
                else:
                    i=i+1
        line=line.split()
        
        if 'if' in line:
            value=EQU_list[EQU_list.index(line[1])+1]
            if value!='0':
                erase_flag1=1
            else:
                erase_flag2=1
                
        if 'else' in line:
            else_flag=1
         
        if erase_flag1==1 and else_flag==1:
            if line[0]=='endif':
                new_test.write(line_copy)
                erase_flag1=0
                else_flag=0
            continue 
        
        if erase_flag2==1:
            if else_flag==1:
                new_test.write(line_copy)
                erase_flag2=0
                else_flag=0
            continue        
            
        new_test.write(line_copy)      
    new_test.close()
    test.close()
    
#Перший перегляд
def FirstScan(asm,new_test, new_analyser, my_lst):
    first_test=open(asm, "r")
    test=open(new_test, "r")                                                      
    analyser=open(new_analyser, "r")                                                        
    out=open(my_lst, "w")
      
    UserIdentifier_list_all=[]
    flag=0
    data_list=[]
    
    for line in analyser:
        line=line.split()
        if line[1]=='data':
            flag=2
            continue
        if flag==2 and line[3]=='user_identifier' and line[0]=='1' :
            data_list.append(line[1])
        if line[1]=='code':
            flag=1
            continue
        if flag==1 and line[3]=='user_identifier' and line[0]=='1' :
            UserIdentifier_list_all.append(line[1])
            continue
        if line[1]=='ends':
            flag=0
            continue
        continue
    
    analyser.seek(0)
    count=0
    line_test=''
    flag=0
    UserIdentifier_list=[]
    EQU=0
    count_str=0
  
    for line in analyser:
        line=line.split()

        if line[0]=='1':
            Out_Scan(out, count, line_test, EQU)
            line_test=test.readline()
            line_first=first_test.readline()
            EQU=0
            while (line_test!=line_first):
                line_first=first_test.readline()
                count_str+=1
            while line_test=='\n':
                Out_Scan(out, count, line_test, EQU)
                line_test=test.readline()
                line_first=first_test.readline()
                count_str+=1
            count_str+=1
            lab=0
            directive=0
            command=''
            register1=0
            register2=0
            register=0
            p=0
            op2=0
            EQU=0
            ERROR=0
            er=0
            mem_flag=0
            seg_reg=0
          
        if line[3]=='user_identifier' and line[0]=='1':
            lab=1
            if line[1]=='code':
                flag=1
                continue
            if flag==1 and line[0]=='1' and line[3]=='user_identifier':
                UserIdentifier_list.append(line[1])
                continue
            if line[1]=='ends':
                flag=0
                continue   
            continue
        
        if line[1]=='equ':
            if line[0]=='2': 
                EQU=1
                continue
            else:
                ERROR=1
                
        if EQU==1:
            count=int(line[1],10)
            continue

        if lab==1:
            if line[3]=='directive':
                directive=1
                if line[1]=='db':
                    inc=1
                    continue
                if line[1]=='dw':
                    inc=2
                    continue
                if line[1]=='dd':
                    inc=4
                    continue
                if line[1]=='segment' or line[1]=='ends':
                    count=0
                    continue

        if lab==1 and directive==1:
            if line[3]=='decimal_number' or line[3]=='hexadecimal_number' or line[3]=='binary_number':
                count+=inc
                continue
            if line[3]=='text_const':
                count+=inc*int(line[2],10)
                continue

        if line[3]=='command' and line[0]=='1':
            if line[1]=='movsd':
                count+=1
                continue
            if line[1]=='inc':
                command='inc'
                continue
            if line[1]=='dec':
                command='dec'
                continue
            if line[1]=='add':
                command='add'
                continue
            if line[1]=='cmp':
                command='cmp'
                continue
            if line[1]=='and':
                command='and'
                continue
            if line[1]=='mov':
                command='mov'
                continue
            if line[1]=='or':
                command='or'
                continue
            if line[1]=='jbe':
                command='jbe'
                continue
        
        #my additional tasks
        if line[3]=='user_identifier' and line[0]=='1':
            lab=1
        if lab==1:
            if line[3]=='directive':
                directive=1
                if line[1]=='db':
                    inc=1
                    continue
                if line[1]=='dw':
                    inc=2
                    continue
                if line[1]=='dd':
                    inc=4
                    continue

        if lab==1 and directive==1:
            if line[3]=='decimal_number' or line[3]=='hexadecimal_number' or line[3]=='binary_number':
                count+=inc
                continue
            if line[3]=='text_const':
                count+=inc*int(line[2],10)
                continue
        #additional tasks ends
        
        if line[3]=='command' and line[0]!='1':
            print('\nERROR: Excess comand(%d)'%count_str)
            
        if command=='inc':
            if line[3]=='32_bit_register':
                count+=1
                continue
            if line[3]=='8_bit_register':
                count+=2
                continue
            if er!=1:
                print('\nERROR: Invalid registers(%d)'%count_str)
                er=1            
            continue
        
        if command=='dec':
            if line[3]=='segment_register':
                seg_reg+=1
                continue
            if line[1]=='byte' or line[1]=='word' or line[1]=='dword' or line[1]=='ptr':
                continue
            if line[1]==':' and seg_reg==1:
                seg_reg+=1
                continue
            #my additional tasks
            if line[1] in data_list:
                count+=6
                continue
            if line[1] in UserIdentifier_list_all:
                count+=7
                continue
            #additional tasks ends
            if line[1]=='[':
                mem_flag+=1
                continue
            if line[3]=='32_bit_register' and (mem_flag==1 or mem_flag==3):
                mem_flag+=1
                continue
            if line[1]=='+' and mem_flag==2:
                mem_flag+=1
                continue
            if line[1]==']' and mem_flag==4:
                mem_flag+=1
            if mem_flag==5:
                if seg_reg==2:
                    count+=4
                    continue
                if seg_reg==0:
                    count+=3
                    continue
                print('\nERROR: Addressing expected(%d)'%count_str)
                continue        
            if er!=1:
                print('\nERROR: Addressing expected(%d)'%count_str)
                er=1
            continue

        if command=='add':
            if line[0]=='2' and line[3]=='32_bit_register':
                register1=32
                continue
            if line[0]=='2' and line[3]=='8_bit_register':
                register1=8
                continue
            if line[0]=='3' and line[1]==',':
                continue
            if line[0]=='4' and line[3]=='32_bit_register':
                register2=32
                if register1==register2:
                    count+=2
                    register1=0
                    register2=0
                    continue
                print('\nERROR: Expected (add reg, reg) (%d)'%count_str)
                continue
            if line[0]=='4' and line[3]=='8_bit_register':
                register2=8
                if register1==register2:
                    count+=2
                    register1=0
                    register2=0
                    continue
                print('\nERROR: Expected (add reg, reg) (%d)'%count_str)
                continue
            if er!=1:
                print('\nERROR: Expected (add reg, reg) (%d)'%count_str)
                er=1
            continue
            
        if command=='cmp':
            if line[3]=='segment_register':
                seg_reg+=1
                continue
            if line[1]==':' and seg_reg==1:
                seg_reg+=1
                continue
            if line[1]=='byte' or line[1]=='word' or line[1]=='dword' or line[1]=='ptr':
                continue
            #my additional tasks
            if line[1] in data_list:
                count+=6
                continue
            if line[1] in UserIdentifier_list_all:
                count+=7
                continue
            #additional tasks ends
            if (line[3]=='32_bit_register' or line[3]=='8_bit_register') and mem_flag==0:
                mem_flag+=1
                continue
            if line[1]==',' and mem_flag==1:
                mem_flag+=1
                continue
            if line[1]=='[' and mem_flag==2:
                mem_flag+=1
                continue
            if line[3]=='32_bit_register' and (mem_flag==3 or mem_flag==5):
                mem_flag+=1
                continue
            if line[1]=='+' and mem_flag==4:
                mem_flag+=1
                continue
            if line[1]==']' and mem_flag==6:
                mem_flag+=1
            if mem_flag==7:
                if seg_reg==2:
                    count+=4
                    continue
                if seg_reg==0:
                    count+=3
                    continue
                print('\nERROR: Expected (cmp reg, mem) (%d)'%count_str)   
                continue
            if er!=1:
                print('\nERROR: Expected (cmp reg, mem) (%d)'%count_str)
                er=1
            continue
            
        if command=='and':
            if line[3]=='segment_register':
                seg_reg+=1
                continue
            if line[1]==':' and seg_reg==1:
                seg_reg+=1
                continue
            if line[1]=='byte' or line[1]=='word' or line[1]=='dword' or line[1]=='ptr':
                continue
            #my additional tasks
            if line[1] in data_list:
                count+=6
                continue
            if line[1] in UserIdentifier_list_all:
                count+=7
                continue
            #additional tasks ends
            if line[1]=='[' and mem_flag==0:
                mem_flag+=1
                continue
            if line[3]=='32_bit_register' and (mem_flag==1 or mem_flag==3):
                mem_flag+=1
                continue
            if line[1]=='+' and mem_flag==2:
                mem_flag+=1
                continue
            if line[1]==']' and mem_flag==4:
                mem_flag+=1
                continue
            if line[1]==',' and mem_flag==5:
                mem_flag+=1
                continue
            if (line[3]=='32_bit_register' or line[3]=='8_bit_register') and mem_flag==6:
                mem_flag+=1
            if mem_flag==7:
                if seg_reg==2:
                    count+=4
                    continue
                if seg_reg==0:
                    count+=3
                    continue
                print('\nERROR: Expected (and mem, reg) (%d)'%count_str)
                continue
            if er!=1:
                print('\nERROR: Expected (and mem, reg) (%d)'%count_str)
                er=1
            continue
                                  
        if command=='mov':
            if line[0]=='2' and line[3]=='32_bit_register':
                register=32
                continue
            if line[0]=='2' and line[3]=='8_bit_register':
                register=8
                continue
            if line[0]=='3' and line[1]==',':
                continue
            if line[0]=='4' and (register==32 or register==8):
                if line[3]=='decimal_number' or line[3]=='hexadecimal_number' or line[3]=='binary_number':
                    if line[3]=='decimal_number':
                        b=int(line[1],10)
                    if line[3]=='hexadecimal_number':
                        j=int(line[2],10)
                        b=int(line[1][0:j-1],16)
                    if line[3]=='binary_number':
                        j=int(line[2],10)
                        b=int(line[1][0:j-1],2)
                    if register==8 and b<256:
                        count+=2
                        continue
                    if register==32:
                        count+=5
                        continue
                    print('\nERROR: Expected (mov reg, imm) (%d)'%count_str)
                    continue
                if er!=1:
                    print('\nERROR: Expected (mov reg, imm) (%d)'%count_str)
                    er=1
                continue
                     
        if command=='or':
            if line[1]=='byte' or line[1]=='word' or line[1]=='dword' or line[1]=='ptr':
                continue
            if line[3]=='segment_register':
                seg_reg+=1
                continue
            if line[1]==':' and seg_reg==1:
                seg_reg+=1
                continue
            if line[1]=='[' and mem_flag==0:
                mem_flag+=1
                continue
            #my additional tasks
            if line[1] in data_list:
                count+=6
                continue
            if line[1] in UserIdentifier_list_all:
                count+=7
                continue
            #additional tasks ends
            if line[3]=='32_bit_register' and (mem_flag==1 or mem_flag==3):
                mem_flag+=1
                continue
            if line[1]=='+' and mem_flag==2:
                mem_flag+=1
                continue
            if line[1]==']' and mem_flag==4:
                mem_flag+=1
                continue
            if line[1]==',' and mem_flag==5:
                mem_flag+=1
                continue    
            if (line[3]=='decimal_number' or line[3]=='hexadecimal_number' or line[3]=='binary_number') and mem_flag==6:
                if line[3]=='decimal_number':
                    b=int(line[1],10)
                if line[3]=='hexadecimal_number':
                    j=int(line[2],10)
                    b=int(line[1][0:j-1],16)
                if line[3]=='binary_number':
                    j=int(line[2],10)
                    b=int(line[1][0:j-1],2)
                if seg_reg==2:
                    if b<=255:
                        count+=5
                        continue
                    else:
                        count+=8
                        continue
                    print('\nERROR: Expected (or mem, imm)(%d)'%count_str)
                    continue
                if seg_reg==0:
                    if b<=255:
                        count+=4
                        continue
                    else:
                        count+=7
                        continue
                    print('\nERROR: Expected (or mem, imm)(%d)'%count_str)
                    continue
                print('\nERROR: Expected (or mem, imm)(%d)'%count_str)
                continue
            if er!=1:
                print('\nERROR: Expected (or mem, imm)(%d)'%count_str)
                er=1
            continue
        
        if command=='jbe':
            if line[1] in UserIdentifier_list:
                count+=2
                continue
            if line[1] in UserIdentifier_list_all:
                count+=6
                continue
            print('\nERROR: Unexpected identifier(%d)'%count_str)
            continue
        
    Out_Scan(out, count, line_test, EQU)
    test.close()
    analyser.close()
    out.close()

#ф-ція виводу першого перегляду                                                        
def Out_Scan(file_out, count, line_test,equ):   
        if equ==1:
            file_out.seek(file_out.tell()-8)
            file_out.write('=%04X'%count)
            file_out.write('   '); 
            file_out.write('%s\n       '%line_test)
        else:
            if 'if' in line_test or 'else' in line_test or 'END' in line_test or 'ends' in line_test:
                if 'END' in line_test:
                    file_out.write('        %s'%line_test)
                elif 'ends' in line_test:
                    file_out.write('%s'%line_test)
                else:
                    file_out.seek(file_out.tell()-8)
                    file_out.write('        %s'%line_test)
                    file_out.write(' %04X'%count)
                    file_out.write('   '); 
            else:
                file_out.write('%s'%line_test)
                file_out.write(' %04X'%count);   file_out.write('   ');   
                
def Out_table(MyLst, out_label):
    LST=open(MyLst, "r")
    out=open(out_label, "w")

    out.write('\n\n')
    out.write('- - - - - - - - - - - - - - - - - - - - - - - - -')
    out.write('\n')
    out.write('%s'%'Name')
    out.write('%15s'%'Size')
    out. write('%10s'%'Length')
    out.write('\n\n')

    label=''
    len_label=''
    for line in LST:
        i=0
        ch=''
        while i < len(line): 
            if line[i] in SingleSymbol: 
                ch=line[i]
                line=line.split(ch,1) 
                line=line[0]+' '+ch+' '+line[1]
                i=i+3 
            else: 
                i=i+1
        line=line.split()

        if 'segment' in line:
            label=line[line.index('segment')-1]

        if 'ends'in line:
            len_label=line[line.index('ends')-2]

        if label!='' and len_label!='':
            out.write('%s'%label)
            out.write('%15s'%'32 bit')
            out.write('%10s'%len_label)
            out.write('\n')
            label=''
            len_label=''
            continue
        continue
    
    out.write('\n')
    out.write('- - - - - - - - - - - - - - - - - - - - - - - - -')
    out.write('\n')
    out.write('%5s'%'Name')
    out.write('%12s'%'Type')
    out.write('%10s'%'Value')
    out.write('%10s'%'Attr')
    out.write('\n\n')
    
    LST.seek(0)
    label=''
    len_label=''
    segment=''
    for line in LST:
        i=0
        ch=''
        while i < len(line): 
            if line[i] in SingleSymbol: 
                ch=line[i]
                line=line.split(ch,1) 
                line=line[0]+' '+ch+' '+line[1]
                i=i+3 
            else: 
                i=i+1
        line=line.split()

        if 'segment' in line:
            segment=line[line.index('segment')-1]
        if 'ends'in line:
            segment=''
            
        lexem=''
        for item in line:
            lexem=item
            lexem_copy=item
            lexem=lexem.lower()
            type_lexem=lexem_analyser(lexem)
            if line[0]=='if' or line[0]=='else' or line[0]=='endif' :
                continue
            if type_lexem=='user_identifier' and line.index(lexem_copy)==1 and 'segment' not in line and 'ends' not in line:

                if line[line.index(lexem_copy)+1]=='db':
                    type_out='BYTE'
                elif line[line.index(lexem_copy)+1]=='dw':
                    type_out='WORD'
                elif line[line.index(lexem_copy)+1]=='dd':
                    type_out='DWORD'
                elif 'EQU' in line:
                    type_out='NOMBER'
                else:
                    type_out='NEAR'
                        
                label=lexem_copy
                out.write('%5s'%label);
                out.write('%12s'%type_out)
                out.write('%10s'%line[0])
                out.write('%10s'%segment)
                out.write('\n')
                continue
    
    LST=open(MyLst,"a")
    out=open(out_label, "r")
    for line in out:
        LST.write('%s'%line)
        
    LST.close()
    out.close()
  
#ініціалізація main
if __name__=="__main__":
    f=''
    f=input('\nEnter identifier file: ')
    
    Analyse(f,'analyser.txt')
    StructLine(f,'struct.txt')
    delete_if_else(f,'new_test.asm')
    Analyse('new_test.asm','new_test_analyser.txt')
    FirstScan(f, 'new_test.asm' , 'new_test_analyser.txt', 'MyLst.txt')
    Out_table('MyLst.txt', 'out_label.txt')
#end
