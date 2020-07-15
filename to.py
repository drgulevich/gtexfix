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

if(re.search('.tex$',args.filename)==None):
    sys.exit('The input should be .tex file. Exit.')

print('LaTeX file:',args.filename)

with open(args.filename, 'r') as source_file:
    source = source_file.read()

### Search for possible token conflicts
conflicts=re.findall('\[ *[012][\.\,][0-9]+\]',source)
if(conflicts!=[]):
    print('Token conflicts detected: ',conflicts)
    sys.exit('Tokens may overlap with the content. Change tokens or remove the source of conflict.')
else:
    print('No token conflicts detected. Proceeding.')

latex=[]
bdoc=re.search(r'\\begin{document}',source)
edoc=re.search(r'\\end{document}',source)
if(bdoc!=None):
    preamble=source[:bdoc.end()]
    latex.append(preamble)
    if(edoc!=None):
        text = '[0.0]' + source[bdoc.end():edoc.start()]
        postamble=source[edoc.start():]
    else:
        text = '[0.0]' + source[bdoc.end():]
        postamble=[]
else:
    text=source.copy()
    postamble=[]

### Treat LaTeX constructs
start_values=[]
end_values=[]
for m in re.finditer(r'\\begin{ *equation\** *}|\\begin{ *figure\** *}|\\begin{ *eqnarray\** *}|\\begin{ *multline\** *}|\\begin{ *thebibliography *}',text):
    start_values.append(m.start())
for m in re.finditer(r'\\end{ *equation\** *}|\\end{ *figure\** *}|\\end{ *eqnarray\** *}|\\end{ *multline\** *}|\\end{ *thebibliography *}',text):
    end_values.append(m.end())
nitems=len(start_values)
assert(len(end_values)==nitems)
if(nitems>0):
    newtext=text[:start_values[0]]
    for neq in range(nitems-1):
        latex.append(text[start_values[neq]:end_values[neq]])
        newtext += '[0.%d]'%(len(latex)-1) + text[end_values[neq]:start_values[neq+1]]
    latex.append(text[start_values[nitems-1]:end_values[nitems-1]])
    newtext += '[0.%d]'%(len(latex)-1) + text[end_values[nitems-1]:]
if(postamble!=[]):
    latex.append(postamble)
    newtext += '[0.%d]'%(len(latex)-1)
with open('gtexfix_latex', 'wb') as fp:
    pickle.dump(latex, fp)
text=newtext

### Treat LaTeX formulas $...$ and $$...$$
# From https://stackoverflow.com/questions/54663900/how-to-use-regular-expression-to-remove-all-math-expression-in-latex-file
reformula = re.compile(r'(\$+)(?:(?!\1)[\s\S])*\1')
formulas=[]
for m in reformula.finditer(text):
    formulas.append(m.group())
nf=0
def repl_f(obj):
    global nf
    nf += 1
    return '[1.%d]'%(nf-1)
text=reformula.sub(repl_f,text)
with open('gtexfix_formulas', 'wb') as fp:
    pickle.dump(formulas, fp)

### Treat LaTeX commands
recommand = re.compile(r'[ ~]*\\cite{[^}]*}|[ ~]*\\citeonline{[^}]*}|[ ~]*\\eqref{\S*}|[ ~]*\\ref{\S*}|[ ~]*\\label{\S*}|\\fi[ \n]|\\newif|\\setlength'
    +r'|\\title|\\chapter|\\section|\\subsection|\\bibliography{[^}]*}|\\bibliographystyle{[^}]*}|\\ifx|\\thispagestyle{\S*}|\\author{[^\}]*}'
    +r'|\\affiliation{[^\}]*}|\\keywords{[^\}]*}|\\begin{ *abstract *}|\\end{ *abstract *}|\\let|\\newpage|\\relax|\\maketitle'
    +r'|\\flushbottom|\\medskip|\\noindent|\\textit|\\degree|\\undefined|\\globalcompile')
commands = recommand.findall(text)
nc=0
def repl_command(obj):
    global nc
    nc += 1
    return  '[2.%d]'%(nc-1)
text=recommand.sub(repl_command,text)
with open('gtexfix_commands', 'wb') as fp:
    pickle.dump(commands, fp)

### Save the processed output to .txt file
limit=30000 # Estimated Google Translate character limit
filebase = re.sub('.tex$','',args.filename)
start=0
npart=0
for m in re.finditer(r'\.\n',text):
    if(m.end()-start<limit):
        end=m.end()
    else:
        output_filename = filebase+'_%d.txt'%npart
        npart+=1
        with open(output_filename, 'w') as txt_file:
	        txt_file.write(text[start:end])
        print('Output file:',output_filename)
        start=end
        end=m.end()
output_filename = filebase+'_%d.txt'%npart
with open(output_filename, 'w') as txt_file:
    txt_file.write(text[start:])
print('Output file:',output_filename)
print('Supply the output file(s) to Google Translate')
