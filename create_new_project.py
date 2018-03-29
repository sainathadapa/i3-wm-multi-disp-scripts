# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import necessaryFuncs as nf

if (len(sys.argv) > 1):
    projectName = sys.argv[1]
else:
    proc = subprocess.Popen(['zenity', '--entry', '--title=I3',
                             "--text=Start a new project with the name:"],
                            stdout=subprocess.PIPE)
    projectName = proc.stdout.read()
    projectName = projectName.decode('utf-8').replace('\n', '').replace('\r', '')

if (projectName is None) or (len(projectName) == 0):
    sys.exit(0)

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))

allOutputs = nf.getListOfOutputs(wkList)

newWorkspaceNums = nf.getValidWorkspaceNums(wkList, len(allOutputs))

commandToRun = ''

wkNameProjectPart = ':' + projectName + ':'

for i in range(1, len(allOutputs) + 1):
    # 1. find a workspace which is on this output
    # 2. switch to it if it is already not focused
    # 3. create the new workspace
    currentWKName = str(newWorkspaceNums[i-1]) + ':' + wkNameProjectPart + str(i)

    currentOutputWK = nf.getWorkspacesOnOutput(wkList, allOutputs[i-1])[0]

    if (i != 1) or (currentOutputWK != nf.getFocusedWK(wkList)):
        commandToRun = commandToRun + 'workspace ' + currentOutputWK + '; '

    commandToRun = commandToRun + 'workspace ' + currentWKName + '; '

commandToRunArray = ['i3-msg', commandToRun]

subprocess.call(commandToRunArray)
