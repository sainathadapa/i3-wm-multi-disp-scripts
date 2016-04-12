# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re

proc = subprocess.Popen(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
proc_out = proc.stdout.read()
wkList = json.loads(proc_out)

def getFocusedWK(wkList):
    return filter(lambda x:x['focused'] == True, wkList)[0]['name']

def getWKNames(wkList):
    return map(lambda x:x['name'], wkList)

def getProjectFromWKName(wkName):
 search_out = re.search(u'^\d+:★(.*)★\d+$', wkName)
 if search_out:
     return search_out.group(1)
 else:
     return None

def getWKNamesFromProj(wkList, projName):
    wknames = getWKNames(wkList)
    return filter(lambda x:getProjectFromWKName(x)==projName, wknames)

focWkName = getFocusedWK(wkList)

def getListOfProjects(wkList):
  wknames = getWKNames(wkList)
  out1 = map(getProjectFromWKName, wknames)
  out2 = filter(lambda x:x != None, out1)
  return list(set(out2))

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

def getVisibleWKs(wkList):
  out1 = filter(lambda x:x['visible'] == True, wkList)
  return map(lambda x:x['name'], out1)

visWks = getVisibleWKs(wkList)

wksToMakeVisible = list(set(nxtProjWks) - set(visWks))

parCommToRun = map(lambda x: u'workspace ' + x, wksToMakeVisible)

commandToRun = [u"i3-msg", u''.join(parCommToRun)]

subprocess.call(commandToRun)
