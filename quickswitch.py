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
        this_node = at.AnyNode(id=con_name, parent=root_node, con_id=root_json['id'])

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
# print(at.RenderTree(root, style=at.AsciiStyle()))

# Displays
displays = [x.id for x in root.children]

# Workspaces
workspaces = [wk
              for display in root.children
              for wk in display.children[0].children]
wknames = [x.id for x in workspaces]
workspaces = [wk.children[0] for wk in workspaces]
for x, y in zip(wknames, workspaces):
    y.id = x

# Get the current workspace
proc_out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], stdout=subprocess.PIPE)
wkList = json.loads(proc_out.stdout.decode('utf-8'))
focWkName = nf.getFocusedWK(wkList)

# Build the final tree
workspaces = [x for x, y in zip(workspaces, wknames) if y != focWkName]
root = at.AnyNode(id='root', con_id=root.con_id)
for a_wk in workspaces:
    a_wk.parent = root
# print(at.RenderTree(root, style=at.AsciiStyle()))

# Create names for containers
[fix_container_names(node) for node in at.PostOrderIter(root)]

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
