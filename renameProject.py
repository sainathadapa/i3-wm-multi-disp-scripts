# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re
from necessaryFuncs import *

proc = subprocess.Popen(['zenity', '--entry', '--title=I3',
    "--text='Rename current project to:'"],
    stdout=subprocess.PIPE)

projectName = proc.stdout.read()

projectName = projectName.replace('\n', '').replace('\r', '')

if (projectName is None) or (len(projectName) == 0):
    sys.exit(0)

proc = subprocess.Popen(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
proc_out = proc.stdout.read()
wkList = json.loads(proc_out)

allWKNames = getWKNames(wkList)

currentWK = getFocusedWK(wkList)

currentProj = getProjectFromWKName(currentWK)

if currentProj is None:
    sys.exit(1)

currentProjWKs = getWKNamesFromProj(wkList, currentProj)

newProjWKs = map(lambda x:x.replace(u"★" + currentProj + u"★",
  u"★" + projectName + u"★"), currentProjWKs)

parCommand = map(lambda (i,x): u'rename workspace ' +
        currentProjWKs[i] + u' to ' +
        newProjWKs[i] + '; ', enumerate(currentProjWKs))

commandToRun = ['i3-msg', ''.join(parCommand)]

subprocess.call(commandToRun)
