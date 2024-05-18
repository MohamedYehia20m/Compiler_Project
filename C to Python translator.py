import re
from graphviz import Digraph

def draw_while_parse_tree(c_code):
    import pycparser
    # Parse the C code into an AST
    parser = pycparser.CParser()
    ast = parser.parse(c_code)

    # Create a Graphviz Digraph
    dot = Digraph()

    # Function to find the first 'while' statement in the AST
    def find_while(node):
        if isinstance(node, pycparser.c_ast.While):
            return node
        for child_name, child in node.children():
            result = find_while(child)
            if result is not None:
                return result
        return None

    # Function to add nodes and edges to the graph
    def add_nodes_edges(node, parent_id=None):
        node_id = str(id(node))
        if isinstance(node, pycparser.c_ast.ID):
            label = node.name
        elif isinstance(node, pycparser.c_ast.BinaryOp):
            label = node.op
        else:
            label = type(node).__name__
        dot.node(node_id, label)

        if parent_id is not None:
            dot.edge(parent_id, node_id)

        for child_name, child in node.children():
            add_nodes_edges(child, node_id)


    # Find the 'while' statement
    while_node = find_while(ast)
    if while_node is None:
        raise ValueError("No 'while' statement found in the provided C code.")

    # Start the recursion from the 'while' node
    add_nodes_edges(while_node)

    # Render the graph to a file and display it
    dot.render('while_parse_tree', view=True, format='png')

# Function to read C code from a file
def read_c_code_from_file(filename):
    with open(filename, 'r') as file:
        c_code = file.read()
    return c_code

# Example usage
filename = 'input.txt'
c_code = read_c_code_from_file(filename)
draw_while_parse_tree(c_code)

#---------line type return funtion-------------------------
def LineTypeFunc():
    code_lines=[]
    line_type=[]
    c=-1
    for line in f:
        c=c+1
        code_lines.append(line[:-1])
        line_type.append(-1)
        line= re.sub('&&',"and",line)
        line= re.sub('\|\|',"or",line)
        line= re.sub('!',"NOT",line)
        if '[' in line and ']' in line:
            if '{' in line:
                line=re.sub('{','[',line)
                line=re.sub('};',']',line)
                a=line
                a=a.split('=')
                b=a[0].split('[')[0]
                line=b+'='+a[1]
            if 'sizeof' in line:
                line = re.sub("sizeof","len",line)
        if(line[0:5]=="print"):
            line_type[c]=4
        if(line[0:2]=="if"):
            line_type[c]=5
        if(line[0:4]=="else"):
            if(line[0:7]=="else if"):
                line_type[c]=6
            else:
                line_type[c]=7
        if(line[0:5]=="while"):
            line_type[c]=9
    return line_type

# Reading from 'input.txt' and writing to 'output.txt'
with open('input.txt', 'r') as input_file:
    with open('output.txt', 'w') as output_file:
        for line in input_file:
            output_file.write(line)

#----------move { to sperate lines------------------------
def process_output_file():
    with open("output.txt", 'r') as input_file, open('bubble.txt', 'w') as output_file:
        for line in input_file:
            if 'printf' not in line:
                line = re.sub(r'{', r'\n{\n', line)
                line = re.sub(r'}', r'\n}\n', line)
            output_file.write(line)

process_output_file()

#--------1. Remove white lines--------------------------
with open("bubble.txt", 'r') as f, open('output.txt', 'w') as ff:
    for line in f:
        if not line.isspace():
            ff.write(line)

#---------2. Remove spaces before lines-------------------------
with open("bubble.txt", 'w') as output_file:
    with open('output.txt', 'r') as input_file:
        for line in input_file:
            if line.startswith(" "):
                first_non_space_index = 0
                for char in line:
                    if char != " ":
                        break
                    first_non_space_index += 1
                cleaned_line = line[first_non_space_index:]
                output_file.write(cleaned_line)
            else:
                output_file.write(line)


#--------4. Spaces in assignment operation--------------------------
with open('bubble.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    line_buffer = ''

    for line in input_file:
        if "print" in line or "while" in line or "if" in line:
            output_file.write(line)
        elif "=" in line:
            if "'" not in line or '"' not in line:
                split_line = line.split()
                for word in split_line:
                    if word[0] != " " and word[-1] != " ":
                        line_buffer += word
                output_file.write(line_buffer + '\n')
                line_buffer = ''
            elif "'" in line or '"' in line:
                line_buffer = ''
                i = 0
                while i != len(line):
                    if line[i] != " " and line[i] != ' ':
                        line_buffer += line[i]
                    if line[i] == "'" or line[i] == '"':
                        i += 1
                        break
                    i += 1
                while i != len(line):
                    line_buffer += line[i]
                    i += 1
                output_file.write(line_buffer + '\n')
                line_buffer = ''
        else:
            output_file.write(line)


#-------5. spaces in variable declearation---------------------------
f= open("output.txt")
line_type=LineTypeFunc()
f.close()

f=open('output.txt')
ff=open('bubble.txt','w')
shub=0
for line in f:
    if line_type[shub]==2:
        a=line
        b=''
        i=0
        while (i!=len(a)):
            if a[i]!=" ":
                b=b+a[i]
            if a[i] == " ":
                b=b+' '
                i+=1
                break
            i+=1
        while (i!=len(a)):
            if a[i] != ' ':
                b=b+a[i]
            i+=1
        c=b.split(',')
        aa=0
        l=''
        for ex in c:
            if '=' in ex:
                l=l+ex.split('=')[0]+','
            else:
                l=l+ex+','
        if '=' in line:
            ff.write(l[:-1]+';'+'\n')
        if '=' not in line:
            ff.write(l[:-1])
        for aa in range(len(c)):
            if "=" in c[aa]:
                if aa!=0 and aa!=len(c)-1:
                    ff.write(c[aa]+';'+'\n')
                elif aa==len(c)-1:
                    ff.write(c[aa])
                elif aa==0:
                    ff.write(c[aa].split()[1]+';'+'\n')
    else:
        ff.write(line)
    shub+=1
ff.close()
f.close()

#--------6. Extra spaces in conditional statements--------------------------
f= open("bubble.txt")
line_type=LineTypeFunc()
f.close()

f=open('bubble.txt')
ff=open('output.txt','w')
shub=0
blank=''

for line in f:
    if line_type[shub]==5:
        for i in line:
            if i!=" ":
                blank=blank+i
        ff.write(blank)
        blank=''
    elif line_type[shub]==9:
        for i in line:
            if i!=" ":
                blank=blank+i
        ff.write(blank)
        blank=''
    else:
        ff.write(line)
        blank=''
    shub+=1

f.close()
ff.close()

#---------8. Extra spaces in print statement.-------------------------
f= open("bubble.txt")
line_type=LineTypeFunc()
f.close()

f=open('bubble.txt')
ff=open('output.txt','w')
shub=0
for line in f:
    if line_type[shub]==3 or line_type[shub]==4:
        if len(line.split('"'))<=3:
            a=line.split('"')
            blank=''
            for i in a[0]:
                if i!=' ':
                    blank+=i
            blank=blank+'"'+a[1]+'"'
            for i in a[2]:
                if i!=' ':
                    blank+=i
            ff.write(blank)
        else:            
            blank=''
            ad=0
            flagg=0
            new=0
            for i in range(len(line)):
                if line[i]=='"':
                    flagg=1
                if flagg==0:
                    if(line[i]!=' '):
                        blank=blank+line[i]
            while(line[new]!='"'):
                new+=1
            start1=new
            for j in range(len(line),0,-1):
                if line[j-1]=='"':
                    break
            end1=j
            while(new!=j):
                blank=blank+line[new]
                new+=1
            while(j!=len(line)):
                if(line[j]!=" "):
                    blank=blank+line[j]
                j+=1
            allx=0
            while(start1+2!=end1-2):
                if(line[start1]=='"'):
                    allx=allx+1
                start1=start1+1
            task=0
            start=-1
            end=len(blank)
            while(start<len(blank)):
                start+=1
                if blank[start]=='"':
                    break
            while(end!=0):
                end-=1
                if blank[end]=='"':
                    break
            blanknew=blank[start+1:end].replace('"','\\"')
            ff.write(blank[:start+1]+blanknew+blank[end:])
    else:
        ff.write(line)
    shub+=1
f.close()
ff.close()

#---------9. adding brackets to loops which dont have-------------------------
f= open("output.txt")
line_type=LineTypeFunc()
f.close()

f=open('output.txt')
ff=open('bubble.txt','w')
shub=0
fflag=0
bflag=0
for line in f:
    if line_type[shub]==5 or line_type[shub]==6 or line_type[shub]==7 or line_type[shub]==9:
        if fflag==1:
            ff.write('{\n'+line)
            bflag+=1
        elif fflag==0:
            ff.write(line)
        fflag=1
    elif '{' in line:
        if fflag==1:
            fflag=0
        ff.write(line)
    else:
        if fflag==1:
            ff.write('{\n'+line+'}\n')
            for i in range(0,bflag):
                ff.write('}\n')
            fflag=0
            bflag=0
        elif fflag==0:
            ff.write(line)
    shub+=1

f.close()
ff.close()

#-------------------------------------------------

def Tx_If(line):
    line=(line+":")
    for xd in range(0,tab_count):
        ff.write('    ')
    ff.write(line)

def Tx_Else(line):
    line=(line+":")
    for xd in range(0,tab_count):
        ff.write('    ')
    ff.write(line)

def Tx_Else_If(line):
    line= re.sub('else if',"elif",line)
    line=(line+":")
    for xd in range(0,tab_count):
        ff.write('    ')
    ff.write(line)

def Tx_While(line):
    line=(line+":")
    for xd in range(0,tab_count):
        ff.write('    ')
    ff.write(line)

def Tx_Printf(line):
    if '",' in line:
        line=line
        a = line.split('"')
        variable = a[2][:-2].split(',')
        newva= variable[1:]
        li= a[1].split("%")
        xxd=[li[0]]
        for i in range(1,len(li)):
            xxd.append(li[i][1:])
        c=0
        for xd in range(0,tab_count):
            ff.write('    ')
        ff.write("print(f'")
        for  i in range (0,len(xxd)-1):
            ff.write(xxd[i])
            ff.write("{"+newva[i]+"}")
            c+=1
        ff.write(li[c][1:]+"')")
    else:
        a = line.split('"')
        linex=a[1]
        for xd in range(0,tab_count):
            ff.write('    ')
        ff.write("print('"+linex+"')")

f= open("bubble.txt")
ff= open('output.txt','w')
code_lines=[]
line_type=[]
c=-1
int_var=[]
float_var=[]
char_var=[]

tab_count=0
for line in f:
    c=c+1
    line_type.append(-1)
    line= re.sub('&&'," and ",line)
    line= re.sub('\|\|'," or ",line)
    line= re.sub('!'," not ",line)
    if "=true" in line:
        line=re.sub('=true',"=True",line)
    if "=false" in line:
        line=re.sub('=false',"=False",line)
    code_lines.append(line[:-1])

    if '[' in line and ']' in line:
        if '{' in line:
            line=re.sub('{','[',line)
            line=re.sub('};',']',line)
            a=line
            a=a.split('=')
            b=a[0].split('[')[0]
            line=b+'='+a[1]
        if 'sizeof' in line:
            line = re.sub("sizeof","len",line)
    if(line[0:5]=="print"):
        line_type[c]=4
    if(line[0:2]=="if"):
        line_type[c]=5
    if(line[0:4]=="else"):
        if(line[0:7]=="else if"):
            line_type[c]=6
        else:
            line_type[c]=7
    if(line[0:5]=="while"):
        line_type[c]=9


for i in range(0,len(code_lines)):
    ff.write('\n')
    if code_lines[i][0]=='{':
        tab_count+=1
        line_type[i] = -2
    if code_lines[i][0]=='}':
        tab_count-=1
        line_type[i] = -2
    if line_type[i] == -1:
        if code_lines[i][-1:]==';':
            code_lines[i]=code_lines[i][:-1]
        for xd in range(0,tab_count):
            ff.write('    ')
        ff.write(code_lines[i])
    elif line_type[i] == 0:
        for xd in range(0,tab_count):
            ff.write('    ')
        ff.write("#"+code_lines[i])
    elif line_type[i] == 4:
        Tx_Printf(code_lines[i])
    elif line_type[i] == 5:
        Tx_If(code_lines[i])
    elif line_type[i] == 6:
        Tx_Else_If(code_lines[i])
    elif line_type[i] == 7:
        Tx_Else(code_lines[i])
    elif line_type[i] == 9:
        Tx_While(code_lines[i])

f.close()
ff.close()


f= open("output.txt")
ff= open('pythonoutput.txt','w')
for line in f:
    if line.isspace()==False:
        ff.write(line)
f.close()
ff.close()


def replace_first_line(file_path, new_line):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Replace the first line with the new string
    lines[0] = new_line + '\n'

    # Write the modified contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

file_path = 'pythonoutput.txt'
new_first_line = 'if __name__ == "__main__":'
replace_first_line(file_path, new_first_line)
