#!/usr/bin/env python
#-----------------------------------------
# Google translate fix for LaTeX documents
# Copyright (c) Dmitry R. Gulevich 2020
# GNU General Public License v3.0
#-----------------------------------------
import re
import sys
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

if(re.search('.txt$',args.filename)==None):
    sys.exit('The input should be .txt file. Exit.')

print('Input file:',args.filename)

### Load LaTeX data from binary files
with open(args.filename, 'r') as fin:
    source = fin.read()
with open ('gtexfix_formulas', 'rb') as fp:
    formulas = pickle.load(fp)
with open ('gtexfix_commands', 'rb') as fp:
    commands = pickle.load(fp)
with open ('gtexfix_latex', 'rb') as fp:
    latex = pickle.load(fp)

### Replace extra characters introduced by translation
trtext=re.sub('\u200B',' ',source)

### Fix spacing
trtext = re.sub(r'\\ ',r'\\',trtext)
trtext = re.sub(' ~ ','~',trtext)

### Restore LaTeX
here=0
newtext=''
clist=[]
flist=[]
llist=[]
nl=0
nf=0
nc=0
corrupted=[]
for m in re.finditer('\[ *[012][\.\,][0-9]+\]',trtext):
    t=int( re.search('(?<=[\[ ])[012](?=[\.\,])',m.group()).group() )
    n=int( re.search('(?<=[\.\,])[0-9]+(?=\])',m.group()).group() )
    if(t==0):
        while(nl!=n):
            corrupted.append('[%d.%d]'%(t,nl))
            nl+=1
        llist.append(n)
        newtext += trtext[here:m.start()] + latex[n]
        nl+=1
    elif(t==1):
        while(nf!=n):
            corrupted.append('[%d.%d]'%(t,nf))
            nf+=1
        flist.append(n)
        newtext += trtext[here:m.start()] + formulas[n]
        nf+=1
    elif(t==2):
        while(nc!=n):
            corrupted.append('[%d.%d]'%(t,nc))
            nc+=1
        clist.append(n)
        newtext += trtext[here:m.start()] + commands[n]
        nc+=1
    here=m.end()
newtext += trtext[here:]
trtext=newtext

### Save the processed output to .tex file
output_filename = re.sub('.txt$','.tex',args.filename)
with open(output_filename, 'w') as translation_file:
	translation_file.write(trtext)
print('Output file:',output_filename)

### Report the corrupted tokens
if(corrupted==[]):
    print('No corrupted tokens. The translation is ready.')	
else:
    print('Corrupted tokens detected:',end=' ')
    for c in corrupted:
        print(c,end=' ')
    print()
    print('To improve the output manually change the corrupted tokens in file',args.filename,'and run from.py again.')
