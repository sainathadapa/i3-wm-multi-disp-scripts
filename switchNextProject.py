#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re
from necessaryFuncs import *

proc_out = subprocess.check_output(['i3-msg', '-t', 'get_workspaces'])
wkList = json.loads(proc_out.decode('utf-8'))

focWkName = getFocusedWK(wkList)

allProjectNames = getListOfProjects(wkList)

if (len(allProjectNames) == 0) or (allProjectNames is None):
  sys.exit(1)

currentProjName = getProjectFromWKName(focWkName)

if currentProjName is None:
  nextProjIndex = 0
else:
  nextProjIndex = allProjectNames.index(currentProjName)

  if nextProjIndex == (len(allProjectNames) - 1):
    nextProjIndex = 0
  else:
    nextProjIndex = nextProjIndex + 1

nxtProjWks = getWKNamesFromProj(wkList, allProjectNames[nextProjIndex])

visWks = getVisibleWKs(wkList)

wksToMakeVisible = list(set(nxtProjWks) - set(visWks))

focOutput = getOutputForWK(wkList, focWkName)
focOutputWks = getWorkspacesOnOutput(wkList, focOutput)
wkToBeFocused = list(set(focOutputWks).intersection(nxtProjWks))

parCommToRun = map(lambda x: 'workspace ' + x, wksToMakeVisible)
if len(wkToBeFocused) > 0 and wksToMakeVisible[-1] != wkToBeFocused[0]:
    parCommToRun.append('workspace ' + wkToBeFocused[0])

commandToRun = ["i3-msg", '; '.join(parCommToRun)]

subprocess.call(commandToRun)

