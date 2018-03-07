# -*- coding: utf-8 -*-
import re


def getWKNames(wkList):
    return [x['name'] for x in wkList]


def getFocusedWK(wkList):
    return [x for x in wkList if x['focused']][0]['name']


def getProjectFromWKName(wkName):
    search_out = re.search('^\d+::(.*):\d+$', wkName)
    if search_out:
        return search_out.group(1)
    else:
        return None


def getWKNamesFromProj(wkList, projName):
    wknames = getWKNames(wkList)
    return [x for x in wknames if getProjectFromWKName(x) == projName]


def getOutputForWK(wkList, wkName):
    return [x for x in wkList if x['name'] == wkName][0]['output']


def getListOfOutputs(wkList):
    outputs_with_duplicates = [x['output'] for x in wkList]
    return list(set(outputs_with_duplicates))


def getWorkspaceNums(wkList):
    return [x['num'] for x in wkList]


def getValidWorkspaceNums(wkList, num):
    wkNums = getWorkspaceNums(wkList)

    if len(wkNums) == 0:
        return None

    maxWKNum = max(wkNums)
    fullWKNums = range(0, maxWKNum + 1)
    goodWKNums = list(set(fullWKNums) - set(wkNums))

    if num <= len(goodWKNums):
        return [goodWKNums[i] for i in range(0, num)]
    else:
        return goodWKNums + list(range(maxWKNum + 1, maxWKNum + 1 + num - len(goodWKNums)))


def getVisibleWKs(wkList):
    return [x['name'] for x in wkList if x['visible']]


def getWorkspacesOnOutput(wkList, outputName):
    return [x['name'] for x in wkList if x['output'] == outputName]


def getListOfProjects(wkList):
    wknames = getWKNames(wkList)
    wknums = getWorkspaceNums(wkList)

    out1 = [getProjectFromWKName(x) for x in wknames]
    out11 = zip(out1, wknums)
    out2 = [x for x in out11 if x[0] is not None]
    listOfProjects = list(set([x[0] for x in out2]))

    def f(x):
        return min([y[1] for y in out2 if y[0] == x])

    out3 = [f(x) for x in listOfProjects]
    sortedProjects = [x for (y, x) in sorted(zip(out3, listOfProjects))]

    return sortedProjects
