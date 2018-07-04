#!/bin/bash
caps="$(xset -q | grep Caps | sed -E "s/ //g;s/[0-9]*//g" | cut -d ":" -f 3)"
if [ "$caps" == "off" ]; then
  echo "caps is off"
  python3 ~/.i3/i3_wm_multi_disp_scripts/focus_next_display.py
else
  echo "caps is on"
  python3 ~/.i3/i3_wm_multi_disp_scripts/switch_to_next_wk_in_project.py
fi
