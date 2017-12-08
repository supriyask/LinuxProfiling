"""
 * file:  stat_parser.py 
 * date:  Wed Dec 06 2017 
 *
 * Description:
 * This script parses the output of 'stat' command on all fds' of all
 * processes and create a complex graph out of it giving a visual of
 * inter-connected processes.
"""


# Import module for graph functions
import itertools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

# Import modules for parsing
import re
import subprocess
from collections import defaultdict

print ("***> Executing 'stat' command...")
print ("It might take a while!") 

# Execute the 'stat' command on all fds' pf all processes
process = subprocess.Popen('stat /proc/*/fd/*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
new = re.sub(u"(\u2018|\u2019)", "'", out.decode('utf-8'))

print ("***> Parsing the output of the command...")

# Parse the output to get the process id and its IPC
fnode = re.compile(r"File:\s+'/proc/(\d*)/fd/\d*'\s+->\s+'(.*)'.*")
fnode_list = fnode.findall(new)
fnode_list = [(x.encode("utf-8"), y.encode("utf-8")) for (x, y) in fnode_list]

fnode_dict = defaultdict(list)
for k, v in fnode_list:
  fnode_dict[v].append(k)

print ("***> Creating a dictionary mapping pid and its IPC")

# Remove slef sockets/pipes, '/dev/*/' communications as well as 'anone_inode' events 
new_dict = {} 
for i in fnode_dict:
  if len(set(fnode_dict[i])) > 1:
    if (not "/dev/" in i and not "anon_inode:[eventfd]" in i): 
      new_dict[i] = fnode_dict[i]
      #print i, set(fnode_dict[i])


# Polish the dict to generate the graph
nodes = []
for i in new_dict:
  nodes = list(set(nodes) | set(new_dict[i]))

print ("***> Generating the graph...")
print ("It might take a while!") 

# Generate the graph and save it as 'complex.png'
count = 1
for i in new_dict:
  cmd = 'G'+str(count)
  cmd=nx.Graph()
  nodes = list(set(new_dict[i]))
  cmd.add_nodes_from(nodes)
  edges = list(itertools.combinations((set(new_dict[i])), r=2))
  cmd.add_edges_from(edges)
  cmd.graph['graph']={'label':i,'labelloc':'t'}
  nx.draw(cmd, node_size=5, node_color = 'green', with_labels = True)
  count += 1
  if count == (len(new_dict.keys()))+1:
    plt.savefig('complex.png')
    break

print ("***> Generated the complex network graph of IPCs!")
print ("***> Graph has been saved as 'complex.png'")
