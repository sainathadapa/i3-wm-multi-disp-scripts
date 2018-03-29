# -*- coding: utf-8 -*-
import subprocess
import json
import necessaryFuncs as nf

proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))

displays = list(sorted(nf.getListOfOutputs(wkList)))
current_display = nf.getOutputForWK(wkList, nf.getFocusedWK(wkList))
current_display_i = [i for i, x in enumerate(displays) if x == current_display][0]

if current_display_i+1 >= len(displays):
    next_display = displays[0]
else:
    next_display = displays[current_display_i + 1]

commandToRun = ["i3-msg", 'focus output ' + next_display]
subprocess.call(commandToRun)
