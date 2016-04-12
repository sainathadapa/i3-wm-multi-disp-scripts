# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re

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

def getWKNames(wkList):
    return map(lambda x:x['name'], wkList)

allWKNames = getWKNames(wkList)

def getFocusedWK(wkList):
    return filter(lambda x:x['focused'] == True, wkList)[0]['name']

currentWK = getFocusedWK(wkList)

def getProjectFromWKName(wkName):
 search_out = re.search(u'^\d+:★(.*)★\d+$', wkName)
 if search_out:
     return search_out.group(1)
 else:
     return None

currentProj = getProjectFromWKName(currentWK)

if currentProj is None:
    sys.exit(1)

def getWKNamesFromProj(wkList, projName):
    wknames = getWKNames(wkList)
    return filter(lambda x:getProjectFromWKName(x)==projName, wknames)

currentProjWKs = getWKNamesFromProj(wkList, currentProj)

newProjWKs = map(lambda x:x.replace(u"★" + currentProj + u"★",
  u"★" + projectName + u"★"), currentProjWKs)

parCommand = map(lambda (i,x): u'rename workspace ' +
        currentProjWKs[i] + u' to ' +
        newProjWKs[i] + '; ', enumerate(currentProjWKs))

commandToRun = ['i3-msg', ''.join(parCommand)]

subprocess.call(commandToRun)
