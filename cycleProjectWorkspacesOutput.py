#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re
from necessaryFuncs import *

proc = subprocess.Popen(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
proc_out = proc.stdout.read()
wkList = json.loads(proc_out)

allWKNames = getWKNames(wkList)

fcsWK = getFocusedWK(wkList)

currentProj = getProjectFromWKName(fcsWK)

if (currentProj == None) or (len(currentProj) == 0):
  sys.exit(1)

currentProjWKs = getWKNamesFromProj(wkList, currentProj)

currentProjWKOutputs = map(lambda x:getOutputForWK(wkList, x), currentProjWKs)
 
newOutputPos =  range(1, len(currentProjWKs) + 1)

def temp(x):
  if (x == len(currentProjWKOutputs)):
    x = 0
  return x

newOutputPos = map(temp, newOutputPos)

newOutputs = map(lambda i:currentProjWKOutputs[i], newOutputPos)

def temp2(i, x):
  ans = ''
  if (i != 0) or (currentProjWKs[i] != getFocusedWK(wkList)):
    ans = ans + 'workspace ' + currentProjWKs[i] + '; '
  ans = ans + 'move workspace to output ' + newOutputs[i] + '; '
  return ans

parCommToRun = map(lambda (i,x):temp2(i,x), enumerate(currentProjWKs))

commandToRun = [u"i3-msg", u''.join(parCommToRun)]

subprocess.call(commandToRun)

