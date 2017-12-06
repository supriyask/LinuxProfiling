from collections import defaultdict
import subprocess
import re

process = subprocess.Popen('stat /proc/*/fd/*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
new = re.sub(u"(\u2018|\u2019)", "'", out.decode('utf-8'))

"""
print ("Sockets:")
sock = re.compile(r"File:\s+'/proc/(\d*)/fd/\d*'\s+->\s+'socket:\[(\d*)\].*")
sock_list = sock.findall(new)
sock_list = [(x.encode("utf-8"), y.encode("utf-8")) for (x, y) in sock_list]

sock_dict = defaultdict(list)
for k, v in sock_list:
  sock_dict[v].append(k)
for i in sock_dict:
  if len(set(sock_dict[i])) > 1:
    print i, set(sock_dict[i])


print ("Pipes:")
pipe = re.compile(r"File:\s+'/proc/(\d*)/fd/\d*'\s+->\s+'pipe:\[(\d*)\].*")
pipe_list = pipe.findall(new)
pipe_list = [(x.encode("utf-8"), y.encode("utf-8")) for (x, y) in pipe_list]

pipe_dict = defaultdict(list)
for k, v in pipe_list:
  pipe_dict[v].append(k)
for i in pipe_dict:
  if len(set(pipe_dict[i])) > 1:
    print i, set(pipe_dict[i])


print ("Inodes:")
inode = re.compile(r"File:\s+`/proc/(\d*)/fd/\d*'.*\n.*\n.*Inode:\s+(\d*)") 
inode_list = inode.findall(new)
inode_list = [(x.encode("utf-8"), y.encode("utf-8")) for (x, y) in inode_list]

inode_dict = defaultdict(list)
for k, v in inode_list:
  inode_dict[v].append(k)
for i in inode_dict:
  if len(set(inode_dict[i])) > 1:
    print i, set(inode_dict[i])
"""

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
    if (not "/dev/" in i and not "pipe" in i and not "anon_inode:[eventfd]" in i): 
    #if (not "anon_inode" in i and not "/dev/" in i): 
    #if (not "anon_inode" in i): 
      new_dict[i] = fnode_dict[i]
      print i, set(fnode_dict[i])

print ("_______________________________________________________________________________________________________________________________________________________________________________")
print ("_______________________________________________________________________________________________________________________________________________________________________________")

import networkx as nx

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import itertools

nodes = []
#for i in fnode_dict:
for i in new_dict:
  nodes = list(set(nodes) | set(new_dict[i]))
#print nodes
print ("_______________________________________________________________________________________________________________________________________________________________________________")

#print fnode_dict['/dev/pts/1']
#G=nx.Graph()
#G.add_nodes_from(nodes)

count = 1
print ("length: ", len(new_dict))
for i in new_dict:
  cmd = 'G'+str(count)
  print cmd
  cmd=nx.Graph()
  nodes = list(set(new_dict[i]))
  cmd.add_nodes_from(nodes)
  edges = list(itertools.combinations((set(new_dict[i])), r=2))
  #print edges
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
    

"""

nodes = []
edges = []
cmd=nx.Graph()
for i in new_dict:
  nodes += (list(set(new_dict[i])))
  edges += (list(itertools.combinations((set(new_dict[i])), r=2)))

cmd.add_nodes_from(nodes)
cmd.add_edges_from(edges)
cmd.graph['graph']={'label':i,'labelloc':'t'}
nx.draw(cmd, node_size=5, node_color = 'green', with_labels = True)
plt.savefig('Complex.png')
plt.show()

if(process.returncode==0):
  lis = (out.strip()).split('\n')
  f = open('processlog', 'w')
  for i in lis:
    print "process ",i,":"
    cmd = 'ls /proc/'+i+'/fd'
    process1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out1, err1 = process1.communicate()
    if (process1.returncode==0):
      list2 = (out1.strip()).split('\n') 
      for fd in list2:
        cmd1 = 'stat /proc/'+i+'/fd/'+fd
        print cmd1
        process2 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = process2.communicate()
        if (process2.returncode==0):
          f.write(out2)
    f.close()
  for i in lis:
"""
