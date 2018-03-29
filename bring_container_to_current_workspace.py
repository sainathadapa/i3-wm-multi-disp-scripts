# -*- coding: utf-8 -*-
import json
import subprocess
import sys
import anytree as at
import necessaryFuncs as nf


def create_tree(root_json, root_node):
    con_name = root_json['name']

    if con_name is None:
        con_name = 'container'

    if con_name in ['__i3', 'topdock', 'bottomdock']:
        return None
    else:
        this_node = at.AnyNode(id=con_name,
                               parent=root_node,
                               con_id=root_json['id'],
                               workspace=False,
                               container=False)

    if con_name == 'container':
        this_node.container = True

    for a_node in root_json['nodes']:
        create_tree(a_node, this_node)


def fix_container_names(node):
    if node.id == 'container':
        node_name = ', '.join([x.id for x in node.children])
        node_name = 'container[' + node_name + ']'
        node.id = node_name


def rofi(options, program):
    '''Call dmenu with a list of options.'''
    cmd = subprocess.Popen(program,
                           shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, _ = cmd.communicate('\n'.join(options).encode('utf-8'))
    return stdout.decode('utf-8').strip('\n')


# Get I3 tree
proc_out = subprocess.run(['i3-msg', '-t', 'get_tree'], stdout=subprocess.PIPE)
i3tree = json.loads(proc_out.stdout.decode('utf-8'))

# Create tree from the i3 tree output
root = at.AnyNode(id='r')
create_tree(i3tree, root)
root = root.children[0]

# Identify the workspaces
for display in root.children:
    for wk in display.children[0].children:
        wk.workspace = True

# Get the current workspace
proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))
focWkName = nf.getFocusedWK(wkList)

# Change the tree such that the workspaces are children to the root
# while ignoring the current workspace
root.children = [node
                 for node in at.PostOrderIter(root, filter_=lambda x: x.workspace)
                 if node.id != focWkName]

# If workspace contains only one container, then remove that container
for node in at.PostOrderIter(root, filter_=lambda x: x.workspace):
    if len(node.children) == 1:
        node.children = node.children[0].children

# If containers have only one element, then remove such containers
for node in at.PreOrderIter(root, filter_=lambda x: x.container):
    if len(node.children) == 1:
        node.children[0].parent = node.parent
        node.parent = None

# Create names for containers
for node in at.PreOrderIter(root, filter_=lambda x: x.container):
    fix_container_names(node)

# Create new names for nodes for diplay in Rofi
names_id_map = [[x+y.id, y.con_id] for x, _, y in at.RenderTree(root)]

# Call rofi
selected = rofi([x[0] for x in names_id_map[1:]], 'rofi -dmenu -i -format i')

if selected == '':
    sys.exit(0)

# Run the command
selected = int(selected)+1
command_to_run = ['i3-msg',
                  '[con_id=' + str(names_id_map[selected][1]) + '] ' +
                  'move --no-auto-back-and-forth container to workspace ' +
                  focWkName]
# print(command_to_run)
subprocess.call(command_to_run)
