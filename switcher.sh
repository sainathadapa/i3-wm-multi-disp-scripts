#!/bin/bash
caps="$(xset -q | grep Caps | sed -E "s/ //g;s/[0-9]*//g" | cut -d ":" -f 3)"
if [ "$caps" == "off" ]; then
  echo "caps is off"
  ~/.i3/i3_wm_multi_disp_scripts/.env/bin/python ~/.i3/i3_wm_multi_disp_scripts/focus_next_display.py
else
  echo "caps is on"
  ~/.i3/i3_wm_multi_disp_scripts/.env/bin/python ~/.i3/i3_wm_multi_disp_scripts/switch_to_next_wk_in_project.py
fi
