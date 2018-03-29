# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import necessaryFuncs as nf

proc = subprocess.Popen(['zenity', '--entry', '--title=I3',
                         "--text=Rename current project to:"],
                        stdout=subprocess.PIPE)

projectName = proc.stdout.read()

projectName = projectName.decode('utf-8').replace('\n', '').replace('\r', '')

if (projectName is None) or (len(projectName) == 0):
    sys.exit(0)

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))

allWKNames = nf.getWKNames(wkList)
currentWK = nf.getFocusedWK(wkList)
currentProj = nf.getProjectFromWKName(currentWK)

if currentProj is None:
    sys.exit(1)

currentProjWKs = nf.getWKNamesFromProj(wkList, currentProj)

newProjWKs = [x.replace(":" + currentProj + ":", ":" + projectName + ":") for x in currentProjWKs]

parCommand = ['rename workspace ' + currentProjWKs[i] + ' to ' + newProjWKs[i] + '; '
              for i, x in enumerate(currentProjWKs)]

commandToRun = ['i3-msg', ''.join(parCommand)]

subprocess.call(commandToRun)
