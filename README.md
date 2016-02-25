*This readme is also present in the form of blog post at http://sainathadapa.github.io/blog/scripts-to-navigate-i3/*

At my workplace, I have a dual monitor setup, with Ubuntu, and [I3](https://i3wm.org/) as the window manager. Being a tiling window manager, I3 allows me to effectively use all the display space, and arrange the windows quickly in different shapes and sizes.

Typically, I have a browser and a terminal (or multiple terminals) on one monitor, and IDE on another. I also generally have multiple such sets of workspaces. Each such set (one workspace for each monitor) represents a project that I am working on. 

This is how the I3 bar looks for me on a typical day:

Monitor 1:
`1:projectA | 3:projectB | 5:projectC`

Monitor 2:
`2:projectA | 4:projectB | 6:projectC`

Now, to switch from working on Project A to Project B, I need to invoke three commands -

(Workspace 1 is focused, Workspace 2 is in a focused inactive state on the other monitor)

1. `$mod+3` to switch to Workspace 3 from Workspace 1 on the first monitor
2. `$mod+2` to focus Workspace 2 on the second monitor
3. `$mod+4` to switch to Worspace 4 from Workspace 2 on the second monitor 

Three commands is an inefficient way to do such a simple & regular task. So, I wrote a script, using which I can achieve the above with one command. This was back in September 2015. Since then, I wrote more scripts to easily navigate and move windows in a multi-monitor setup with I3. And yes, it also works with more than two monitors.

# Where
The project is located at [github.com/sainathadapa/i3-project-focus-workflow](https://github.com/sainathadapa/i3-project-focus-workflow).

# How to install
1. Install NodeJS, NPM and Coffeescript (`apt-get install nodejs npm coffeescript`)
2. Clone the project (`git clone git@github.com:sainathadapa/i3-project-focus-workflow.git`)
3. `cd .i3/i3-project-focus-workflow/; npm install`
4. Bind the scripts to shortcut keys in the I3 config file

You can also directly install from [npm](https://www.npmjs.com/package/i3-project-focus-workflow).`npm install i3-project-focus-workflow`

# Terminology
A project is defined as a set of workspaces, one workspace for each display/monitor available.

# Usage

## newProjectWorkspaces.coffee

To create a new project, run the `newProjectWorkspaces.coffee` script. This will display a dialog box asking for the project name. Names of the workspaces will contain the project name.

Dialog box:
![New project dialog box](img/new_project_dialog.png)

After:
![New set of workspaces](img/new_project_after.png)

## renameProject.coffee

To rename a project, run `renameProject.coffee`. This will display a dialog box asking for the new project name.

Dialog box:
![Rename project dialog box](img/rename_project_dialog.png)

After:
![After rename](img/rename_project_after.png)

## switchNextProject.coffee

To switch to the next project, run `switchNextProject.coffee`

## cycleProjectWorkspacesFocus.coffee

To cycle the focus between the workspaces in a project, run `cycleProjectWorkspacesFocus.coffee`

## cycleProjectWorkspacesOutput.coffee

To shift all the workspaces in a project to each one's respective next display, run `cycleProjectWorkspacesOutput.coffee`. For example, if the initial state of the workspaces is {Wksp 1 - Disp 1}, {Wksp 2 - Disp 2}, {Wksp 3 - Disp 3}, after running the script, the final state will be {Wksp 1 - Disp 2}, {Wksp 2 - Disp 3}, {Wksp 3 - Disp 1}.

Initial state:
![Initial state](img/initial_state.png)

After running the script:
![After workspace switch](img/after_cycle_workspace_display.png)

## cycleContainerProjectWorkspaces.coffee

To switch the focused container to the next workspace in the project, run `cycleContainerProjectWorkspaces.coffee`.

Initial state:
![Initial state](img/initial_state.png)

After running the script:
![Gvim moved](img/after_cycle_container.png)

# Sample I3 config
To use the scripts, add these lines to your I3 config:

``` sh
# project workflow bindings
bindsym $mod+Shift+p exec coffee ~/.i3/i3-project-focus-workflow/newProjectWorkspaces.coffee
bindsym $mod+p exec coffee ~/.i3/i3-project-focus-workflow/switchNextProject.coffee
bindsym $mod+Tab exec coffee ~/.i3/i3-project-focus-workflow/cycleProjectWorkspacesFocus.coffee
bindsym $mod+Shift+Tab exec coffee ~/.i3/i3-project-focus-workflow/cycleProjectWorkspacesOutput.coffee
bindsym $mod+Control+Tab exec coffee ~/.i3/i3-project-focus-workflow/cycleContainerProjectWorkspaces.coffee
bindsym $mod+n exec coffee ~/.i3/i3-project-focus-workflow/renameProject.coffee

# create a initial project on startup with project name 'default'
exec --no-startup-id coffee ~/.i3/i3-project-focus-workflow/newProjectWorkspaces.coffee default
```

 
