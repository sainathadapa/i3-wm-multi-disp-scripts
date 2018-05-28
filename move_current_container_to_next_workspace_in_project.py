# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import necessaryFuncs as nf

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))

allWKNames = nf.getWKNames(wkList)

currentWK = nf.getFocusedWK(wkList)

currentProj = nf.getProjectFromWKName(currentWK)

if currentProj is None:
    sys.exit(1)

currentProjWKs = nf.getWKNamesFromProj(wkList, currentProj)

if len(currentProjWKs) < 2:
    sys.exit(1)

thisWKPos = currentProjWKs.index(currentWK)

newWKPos = thisWKPos + 1
if newWKPos == len(currentProjWKs):
    newWKPos = 0

commandToRun = ['i3-msg', 'move container to workspace ' + currentProjWKs[newWKPos]]

subprocess.call(commandToRun)
