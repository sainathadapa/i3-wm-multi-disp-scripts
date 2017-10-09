#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re
from necessaryFuncs import *

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))

allWKNames = getWKNames(wkList)

fcsWK = getFocusedWK(wkList)

currentProj = getProjectFromWKName(fcsWK)

if (currentProj == None) or (len(currentProj) == 0):
  sys.exit(1)

currentProjWKs = getWKNamesFromProj(wkList, currentProj)

currentProjWKOutputs = [getOutputForWK(wkList, x) for x in currentProjWKs]
 
newOutputPos =  range(1, len(currentProjWKs) + 1)

def newOutputPosFn(x):
  if (x == len(currentProjWKOutputs)):
    x = 0
  return x

newOutputPos = [newOutputPosFn(x) for x in newOutputPos]

newOutputs = [currentProjWKOutputs[i] for i in newOutputPos]

def mk_cmd(i, x):
  ans = ''
  if (i != 0) or (currentProjWKs[i] != getFocusedWK(wkList)):
    ans = ans + 'workspace ' + currentProjWKs[i] + '; '
  ans = ans + 'move workspace to output ' + newOutputs[i] + '; '
  return ans

parCommToRun = [mk_cmd(i,x) for i,x in enumerate(currentProjWKs)]

commandToRun = ["i3-msg", ''.join(parCommToRun)]

subprocess.call(commandToRun)

