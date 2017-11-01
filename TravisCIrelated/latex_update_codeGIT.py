'''
update a code within tex file, by injecting 
the updated code in a source.

This scrip was written for syncing changes in .ijm / .py / .m file 
to the corresponding code that appears in latex file. 

It first scans though fragmented tex file in Authorea repository.
Check each tex file for the file name of the code. 
When found, the code in tex file is replaced with that in the
source code file.

20171027 Kota @ NEUBIAS WG6 project
'''

import fileinput
import re, os, sys
from git import Repo

#argfilename = sys.argv[1] # source code file. It could be a relative path. 

def processOneFile(targettex, previousfile, filename):
    ffile = os.path.basename(targettex)
    fbasename = os.path.splitext(targettex)[0] # filename without extension
    #parentdir = os.path.dirname(targettex)
    lines  = [line.rstrip('\n') for line in open(targettex)]
    out =  ''
    replaced = False
    codetexfile = targettex
    for index, ll in enumerate(lines):
        matched = re.search(r"\\textbf{sourcecode}.*" + filename, ll)
        if matched:
            if index == 0:
                codetexfile = previousfile
            print "code file: ", codetexfile
            #print matched.group(1)
            print ll
            with open(codetexfile, 'r') as file:
                content = file.read()
            with open(os.path.join(parentdir, filename)) as file:
                source = file.read()
            content = re.sub(r"(\\begin\{lstlisting\}.*\n)((.*\n)+)(\\end{lstlisting})", "\g<1>" + source + "\n\g<4>", content)
            print content
            replaced = True
            with open(codetexfile, 'w') as file:
                file.write(content)
            break
    #if not replaced:
        #print("... No Match found!: ")


            #content =             #codedata = codef.read()
        #else:
            #print "No Match"
    #print out
    #f2 = open(f, 'w')
    #f2.write(out)
    #f2.close()

def batchProcessTexFiles(layoutmd, argfilename):
    #parentdir = os.path.dirname(layoutmd)
    filename = os.path.basename(argfilename) # filename without path
    print("Update tex files based on changes in " + filename)
    lines  = [line.rstrip('\n') for line in open(layoutmd)]
    for index, ll in enumerate(lines):
        if ll.endswith('.tex'):
            previousfile = ""
            if index > 0:
                previousfile = os.path.join(parentdir, lines[index - 1])

            targettex = os.path.join(parentdir, ll)
            print "Checking: ", targettex
            #print "... Previous Tex: ", previousfile
            processOneFile(targettex, previousfile, filename)
        #else:
            #print ll


repo = Repo("./")
updatedfiles = repo.git.diff('HEAD~1..HEAD', name_only=True)
updatedlist = updatedfiles.split("\n")
updatestatus = False
for f in updatedlist:
    if f.endswith(".ijm") or f.endswith(".m"):
        if os.path.isfile(f):
            parentdir = os.path.dirname(f)
            layoutmd = os.path.join(parentdir, "layout.md")
            if os.path.isfile(layoutmd):
                print("A commit with " + f + " detected")
                updatestatus = True
                batchProcessTexFiles(layoutmd, f)
            else:
                print("layout.md does not exists")
        else:
            print("File Does Not Exist: " + f)
if not updatestatus:
    print("Code updator: No commit with code updates.")

#processOneFile(f)


