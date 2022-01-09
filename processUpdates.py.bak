import json
import os
from pathlib import Path
import glob
import re

cwd = os.getcwd()
latex_files = os.path.join(cwd,"latex-code\*.tex")

with open('indexupdates.json', 'r') as f:
    data = json.load(f)
    #print(data)
    for update in data["updates"]:
        found_file_bool = False
        txtfiles = []
        for file in glob.glob(latex_files):
            #print(file)
            txtfiles.append(file)
        #print(update["sender"])
        #print(update["subject"])
        #print(update["text"])
        #print(update["htmltext"])
        if update["implemented"] == "false":
            #print("need to process: ")
            #print(update["text"])
            commands = ""
            
            for line in update["text"].split("\n"):
                if found_file_bool == False:
                     #print("newline")
                     #print(line)
                     for file in txtfiles:
                        if re.search(line.replace("\r",""),file) != None:
                            #print(file)
                            found_file = file
                            found_file_bool = True
                else:
                    commands += "\n"
                    commands += line
                    #if line in file:  
                    #    print("found")
                    #    print(line)
                #search for line in tex files
                 

            print("will update commands:")
            print(commands)
            print(found_file)

            with open(found_file, 'r') as texfile:
                texdata = texfile.read()
                texdata += '\n\\textbf{neuer Befehl}\\begin{lstlisting}'
                for command in commands.split("\n"):
                    texdata += '\n'
                    texdata += command
                texdata += '\end{lstlisting}'
                #texfile.write(texdata)
                print(texdata)
                #\textbf{HTML zu Text umwandeln}
                #\begin{lstlisting}
            with open(found_file, 'w') as texfile:
                texfile.write(texdata)
            update["implemented"]="true"
    

    


    


            

with open('indexupdates.json', 'w') as f:
    json.dump(data, f)
