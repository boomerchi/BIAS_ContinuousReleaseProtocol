'''
injecting ijm code into tex file. 
scans though fragmented tex file in Authorea repository
sourced ijm file using \lstinputlisting is loaded and 
replaced with codes bounded by \lstlisting
20171021 Kota @ NEUBIAS WG6 project
'''

import fileinput
import re, os, sys

argfilename = sys.argv[1] # assume that the first argument is the file name
#f = 'mod2all.tex'

def processOneFile(f):
    ffile = os.path.basename(f)
    fbasename = os.path.splitext(f)[0] # filename without extension
    outfilename = fbasename + 'WithCodes.tex'
    parentdir = os.path.dirname(f)
    lines  = [line.rstrip('\n') for line in open(f)]
    out =  ''
    for ll in lines:
        matched = re.match(r"(.*)\\lstinputlisting(\[.*\])?{(.*\.ijm)}", ll)
        if matched:
            # print matched.group()
            pref = matched.group(1)
            options = matched.group(2)
            contents = matched.group(3)
            contents = os.path.join( parentdir, os.path.basename(contents)) # in Authorea, ijm files are moved to the root
            print contents
            codef = open(contents, 'r')
            codedata = codef.read()

            if not options:
                options = ''
            newtext = pref + '\n' \
                    '\\begin{lstlisting}' + options + '\n' + \
                    codedata + '\n' + \
                    '\\end{lstlisting}' + '\n' \
                    '\\textbf{sourcecode}: ' + contents
            # print newtext
            out = out + newtext + '\n'
            codef.close()
        else:
            out = out + ll + '\n'

    #print out
    #f2 = open(outfilename, 'w')
    f2 = open(f, 'w')
    f2.write(out)
    f2.close()

def batchProcessTexFiles(layoutmd):
    parentdir = os.path.dirname(layoutmd)
    lines  = [line.rstrip('\n') for line in open(layoutmd)]
    for ll in lines:
        if ll.endswith('.tex'):
            targettex = os.path.join(parentdir, ll)
            print targettex
            processOneFile(targettex)
        else:
            print ll


#f = 'mod3merged.tex'
#f = argfilename
layoutmd = argfilename
batchProcessTexFiles(layoutmd)
#processOneFile(f)


