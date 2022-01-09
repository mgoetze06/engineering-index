from imap_tools import MailBox, AND
import html2text
import json
import os
from pathlib import Path

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
mb = MailBox(server).login(user, password)


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

        
    # Print the plain text (if there is one)
    #print(msg.text)
    # Add attachments
    #files += [att.payload for att in msg.attachments if att.filename.endswith('.pdf')]
