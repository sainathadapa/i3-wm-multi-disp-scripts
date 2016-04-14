#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
from necessaryFuncs import *

proc = subprocess.Popen(['zenity', '--entry', '--title=I3', 
  "--text='Start a new project with the name:'"],
  stdout=subprocess.PIPE)

projectName = proc.stdout.read()

projectName = projectName.replace('\n', '').replace('\r', '')

if (projectName is None) or (len(projectName) == 0):
  sys.exit(0)

proc = subprocess.Popen(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
proc_out = proc.stdout.read()
wkList = json.loads(proc_out)

allOutputs = getListOfOutputs(wkList)

newWorkspaceNums = getValidWorkspaceNums(wkList, len(allOutputs))

commandToRun = ''

wkNameProjectPart = '★' + projectName + '★'

for i in range(1, len(allOutputs) + 1):
  # 1. find a workspace which is on this output
  # 2. switch to it if it is already not focused
  # 3. create the new workspace
  currentWKName = str(newWorkspaceNums[i-1]) + ':' + wkNameProjectPart + str(i)

  currentOutputWK = getWorkspacesOnOutput(wkList, allOutputs[i-1])[0]

  if (i != 1) or (currentOutputWK != getFocusedWK(wkList)) :
    commandToRun = commandToRun + 'workspace ' + currentOutputWK + '; '

  commandToRun = commandToRun.encode('utf-8') + 'workspace ' + currentWKName + '; '

commandToRunArray = ['i3-msg', commandToRun]

subprocess.call(commandToRunArray)
