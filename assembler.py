#Give the location of the .asm file to the 'f1' variable provided. 

import sys
import os
import re

f1 = open(os.path.join(r'C:\Users\peddireddy\OneDrive - Amrita Vishwa Vidyapeetham\Desktop\nand2tetris\projects\06\max\MaxL.asm'), "r")
f2 = open(os.path.join(r'E:\SEM-2\eoc\maxl_2.hack'), "w")

table = {}
symbol_table={}
dest_table={}
jmp_table={}

symbol_table['0']='101010'
symbol_table['1']='111111'
symbol_table['-1']='111010'
symbol_table['D']='001100'
symbol_table['A']='110000'
symbol_table['M']='110000'
symbol_table['!D']='001101'
symbol_table['!A']='110001'
symbol_table['!M']='110001'
symbol_table['-D']='001111'
symbol_table['-A']='110011'
symbol_table['D+1']='011111'
symbol_table['A+1']='110111'
symbol_table['M+1']='110111'
symbol_table['D-1']='001110'
symbol_table['A-1']='110010'
symbol_table['M-1']='110010'
symbol_table['D+A']='000010'
symbol_table['A+D']='000010'
symbol_table['D+M']='000010'
symbol_table['M+D']='000010'
symbol_table['D-A']='010011'
symbol_table['D-M']='010011'
symbol_table['A-D']='000111'
symbol_table['A-M']='000111'
symbol_table['D&A']='000000'
symbol_table['D&M']='000000'
symbol_table['A&D']='000000'
symbol_table['M&D']='000000'
symbol_table['D|A']='010101'
symbol_table['A|D']='010101'
symbol_table['D|M']='010101'
symbol_table['M|D']='010101'

dest_table['M']='001'
dest_table['D']='010'
dest_table['MD']='011'
dest_table['A']='100'
dest_table['AM']='101'
dest_table['AD']='110'
dest_table['AMD']='111'

jmp_table['JGT']='001'
jmp_table['JEQ']='010'
jmp_table['JGE']='011'
jmp_table['JLT']='100'
jmp_table['JNE']='101'
jmp_table['JLE']='110'
jmp_table['JMP']='111'

def convert(all_lines):
    index=0
    new_set_lines=[]
    for line in all_lines:
        if line[0]=='(':
            text = line[1:-1]
            table[text]=index
            all_lines.remove(line)
        index += 1

    index=0
    curr_mem = 16
    for line in all_lines:
        if line[0]=='@':
            text = line[1:]
            if text=='R0' or text=='R1' or text=='R2' or text=='R3' or text=='R4' or text=='R5' or text=='R6' or text=='R7' or text=='R8' or text=='R9' or text=='R10' or text=='R11' or text=='R12' or text=='R13' or text=='R14' or text=='R15':
                num = text[1:]
                new_set_lines.append('@'+num)
            elif text.isnumeric():
                new_set_lines.append(line)
            else:
                text=line[1:]
                num = table.get(text)
                if num is not None:
                    new_set_lines.append('@'+str(num))
                else:
                    new_set_lines.append('@'+str(curr_mem))
                    table[line[1:]] = curr_mem
                    curr_mem = curr_mem + 1
                
        elif line[0]=='(':
            index += 1
            continue
        
        else:
            new_set_lines.append(line)
                
        index += 1
    return new_set_lines           

def A_instruction(line):
    binary_num = bin(int(line[1:]))
    num = binary_num[2:]
    print(num.zfill(16))
    f2.write(num.zfill(16))
    f2.write('\n')
    

def C_instruction(line):
    index=line.find(';')
    final_text='111'
    if index==-1:
        index_eq = line.find('=')
        dest = line[:index_eq]
        value = line[index_eq+1:]
        if value.find('M')!=-1:
            final_text+='1'
            final_text+=symbol_table.get(value)
            final_text+=dest_table.get(dest)
            final_text+='000'
        else:
            final_text+='0'
            final_text+=symbol_table.get(value)
            final_text+=dest_table.get(dest)
            final_text+='000'

    else:
        index_sc = line.find(';')
        value = line[:index_sc]
        jmp_dest = line[index_sc+1:]
        if value.find('M')!=-1:
            final_text+='1'
            final_text+=symbol_table.get(value)
            final_text+='000'
            final_text+=jmp_table.get(jmp_dest)
        else:
            final_text+='0'
            final_text+=symbol_table.get(value)
            final_text+='000'
            final_text+=jmp_table.get(jmp_dest)

    print(final_text)
    f2.write(final_text)
    f2.write('\n')

def check_A_C_instruction(new_set_lines):
    for line in new_set_lines:
        if line[0]=='@':
            A_instruction(line)
        else:
            C_instruction(line)

all_lines=[]
for lines in f1:
    new_line = ((lines.replace('\n','')).replace(' ','')).replace('\t','')
    new_line=re.sub('//.*','',str(new_line))
    if new_line!='': 
        all_lines.append(new_line)

new_set_lines = convert(all_lines)
print(new_set_lines)
check_A_C_instruction(new_set_lines)
f1.close()
f2.close()
