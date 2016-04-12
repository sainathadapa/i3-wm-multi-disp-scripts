# -*- coding: utf-8 -*-
import subprocess
import json
import sys

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

def getListOfOutputs(wkList):
  outputs_with_duplicates = map(lambda x:x['output'], wkList)
  return list(set(outputs_with_duplicates))

allOutputs = getListOfOutputs(wkList)

def getWorkspaceNums(wkList):
  return map(lambda x:x['num'], wkList)

def getValidWorkspaceNums(wkList, num):
  num = num + 1
  wkNums = getWorkspaceNums(wkList)

  if len(wkNums) == 0 :
    return None

  maxWKNum = max(wkNums)
  fullWKNums = range(0, maxWKNum + 1)
  goodWKNums = list(set(fullWKNums) - set(wkNums))

  if num <= len(goodWKNums):
    return [[goodWKNums][i] for i in range(0, num + 1)]
  else:
    return goodWKNums + range(maxWKNum + 1, maxWKNum + num + 1 - len(goodWKNums))

newWorkspaceNums = getValidWorkspaceNums(wkList, len(allOutputs))


commandToRun = ''

wkNameProjectPart = '★' + projectName + '★'


def getWorkspacesOnOutput(wkList, outputName):
  filteredObj = filter(lambda x:x['output'] == outputName, wkList)
  return map(lambda x:x['name'], filteredObj)

def getFocusedWK(wkList):
  return filter(lambda x:x['focused'] == True, wkList)[0]['name']

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
