from imap_tools import MailBox, AND
import html2text
import json
import os
from pathlib import Path
import json
import os
from pathlib import Path
import glob
import re

def update_text_file_from_json():
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
                    texdata += '\n\\textbf{neuer Befehl}\\begin{lstlisting}\n'
                    for command in commands.split("\n"):
                        #texdata += '\n'
                        texdata += command
                    texdata += '\end{lstlisting}'
                    #texfile.write(texdata)
                    print(texdata)
                    #\textbf{HTML zu Text umwandeln}
                    #\begin{lstlisting}
                with open(found_file, 'w') as texfile:
                    texfile.write(texdata)
                update["implemented"]="true"
            else:
                print("Update in JSON enthalten, aber schon implementiert.")
    with open('indexupdates.json', 'w') as f:
        json.dump(data, f)

def read_imap_server_to_json():
    # Server is the address of the imap server

    cwd = os.getcwd()
    path = Path(cwd)

    parentPath = path.parent.absolute()
    print(parentPath)
    import sys
    ## insert at 1, 0 is the script path (or '' in REPL)
    sys.path.append(path.parent.absolute())
    print(sys.path.append(path.parent.absolute()))
    fullpath = os.path.join(parentPath, "index_config.txt")
    with open(fullpath, 'r') as f:
        lines = f.readlines()
        user = lines[0].replace('\n', '')
        password = lines[1].replace('\n', '')

    server = "imap.web.de"
    mb = MailBox(server).login("engineering-index@web.de", "mengineeringindex06")


    #messages = mb.fetch(criteria=AND(seen=False, from_="electricity.com"),
    #                      mark_seen=False,
    #                       bulk=True)
    messages = mb.fetch(criteria = 'ALL',mark_seen=False,bulk=True)
    #files = []
    for msg in messages:
        # Print form and subject
        print(msg.from_, ': ', msg.subject)

        if "Update Index" in msg.subject:
            print("Updating Index ....")
            #print(msg.text)
            htmltext = html2text.html2text(msg.html)
            print(htmltext)
            #print(msg)

            #new python object
            x = {
                "sender": msg.from_,
                "subject": msg.subject,
                "htmltext": htmltext,
                "text": msg.text,
                "implemented": "false"
            }
            with open('indexupdates.json', 'r+') as f:
                data = json.load(f)
                data["updates"].append(x)
                f.seek(0)
                json.dump(data, f)
            
            output = json.dumps(x)
            print(output)
            #verschieben der mail, wenn sie verarbeitet wurde (beim nächsten mal nicht mehr berücksichtigen
            mb.move(msg.uid, 'Verarbeitet')
        else:
            print("Email gefunden, aber kein Index Update")
            
        # Print the plain text (if there is one)
        #print(msg.text)
        # Add attachments
        #files += [att.payload for att in msg.attachments if att.filename.endswith('.pdf')]

def main():
    read_imap_server_to_json()
    update_text_file_from_json()

if __name__ == '__main__':
    main()


