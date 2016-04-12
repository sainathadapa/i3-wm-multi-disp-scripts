# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import re

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

def getListOfOutputs(wkList):
  outputs_with_duplicates = map(lambda x:x['output'], wkList)
  return list(set(outputs_with_duplicates))

def getWKNames(wkList):
    return map(lambda x:x['name'], wkList)

def getFocusedWK(wkList):
  return filter(lambda x:x['focused'] == True, wkList)[0]['name']

def getVisibleWKs(wkList):
  out1 = filter(lambda x:x['visible'] == True, wkList)
  return map(lambda x:x['name'], out1)

def getWorkspacesOnOutput(wkList, outputName):
  filteredObj = filter(lambda x:x['output'] == outputName, wkList)
  return map(lambda x:x['name'], filteredObj)

def getListOfProjects(wkList):
  wknames = getWKNames(wkList)
  out1 = map(getProjectFromWKName, wknames)
  out2 = filter(lambda x:x != None, out1)
  return list(set(out2))

def getProjectFromWKName(wkName):
 search_out = re.search(u'^\d+:★(.*)★\d+$', wkName)
 if search_out:
     return search_out.group(1)
 else:
     return None

def getWKNamesFromProj(wkList, projName):
    wknames = getWKNames(wkList)
    return filter(lambda x:getProjectFromWKName(x)==projName, wknames)

def getWorkspaceNums(wkList):
  return map(lambda x:x['num'], wkList)

def getOutputForWK(wkList, wkName):
    return filter(lambda x:x['name'] == wkName)[0]['output']
