import subprocess
import re
import networkx as nx

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import itertools
from collections import defaultdict

process = subprocess.Popen('stat /proc/*/fd/*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
new = re.sub(u"(\u2018|\u2019)", "'", out.decode('utf-8'))

print ("Filename matching:")
fnode = re.compile(r"File:\s+'/proc/(\d*)/fd/\d*'\s+->\s+'(.*)'.*")
fnode_list = fnode.findall(new)
fnode_list = [(x.encode("utf-8"), y.encode("utf-8")) for (x, y) in fnode_list]

fnode_dict = defaultdict(list)
for k, v in fnode_list:
  fnode_dict[v].append(k)
new_dict = {} 
for i in fnode_dict:
  if len(set(fnode_dict[i])) > 1:
    if (not "/dev/" in i and not "anon_inode:[eventfd]" in i): 
      new_dict[i] = fnode_dict[i]
      print i, set(fnode_dict[i])

print ("_______________________________________________________________________________________________________________________________________________________________________________")


nodes = []
for i in new_dict:
  nodes = list(set(nodes) | set(new_dict[i]))

count = 1
print ("length: ", len(new_dict))
for i in new_dict:
  cmd = 'G'+str(count)
  print cmd
  cmd=nx.Graph()
  nodes = list(set(new_dict[i]))
  cmd.add_nodes_from(nodes)
  edges = list(itertools.combinations((set(new_dict[i])), r=2))
  print ("_______________________________________________________________________________________________________________________________________________________________________________")
  cmd.add_edges_from(edges)
  cmd.graph['graph']={'label':i,'labelloc':'t'}
  nx.draw(cmd, node_size=5, node_color = 'green', with_labels = True)
  #plt.savefig('Graph'+str(count)+'.png')
  #plt.show()
  count += 1
  if count == (len(new_dict.keys()))+1:
    plt.savefig('complex.png')
    break
