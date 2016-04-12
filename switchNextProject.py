# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re
from necessaryFuncs import *

proc = subprocess.Popen(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
proc_out = proc.stdout.read()
wkList = json.loads(proc_out)

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

parCommToRun = map(lambda x: u'workspace ' + x, wksToMakeVisible)

commandToRun = [u"i3-msg", u''.join(parCommToRun)]

subprocess.call(commandToRun)
