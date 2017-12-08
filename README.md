### Analyzing run-time process interactions to model a complex network for threat identification

#### Description:

This script parses the output of 'stat' command on all fds' of all processes and create a complex graph out of it giving a visual of inter-connected processes.

#### Example:

Let us consider an example of pipe between two processes.
```
root@ubuntu:/home/supriya# grep "example pipe" | grep "print it to the stdout"
```
```
root@ubuntu:~# stat /proc/2497/fd/1
  File: ‘/proc/2497/fd/1’ -> ‘pipe:[19040]’
  Size: 64           Blocks: 0          IO Block: 1024   symbolic link
Device: 4h/4d        Inode: 19420       Links: 1
Access: (0300/l-wx------)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2017-12-07 17:19:01.262765577 -0800
Modify: 2017-12-07 17:19:01.262765577 -0800
Change: 2017-12-07 17:19:01.262765577 -0800
  Birth: -
```
```
root@ubuntu:~# ps awuxx | grep grep
root   2497  0.0  0.2  15944  2236 pts/13   S+   17:18   0:00 grep --color=auto example pipe
root   2498  0.0  0.2  15944  2244 pts/13   S+   17:18   0:00 grep --color=auto print it to the stdout
```
```
root@ubuntu:~# stat /proc/2498/fd/0
  File: ‘/proc/2498/fd/0’ -> ‘pipe:[19040]’
  Size: 64           Blocks: 0          IO Block: 1024   symbolic link
Device: 4h/4d        Inode: 19427       Links: 1
Access: (0500/lr-x------)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2017-12-07 17:19:07.966115817 -0800
Modify: 2017-12-07 17:19:07.966115817 -0800
Change: 2017-12-07 17:19:07.966115817 -0800
  Birth: -
```

#### Explanation:

The script captures ‘pipe:[19040]’ and connects all processes (2497 and 2498)  using this.
The output of first part - the parser is a dictionary mapping IPCs to its corresponding processes.

For the above example, the output looks like -
```
> print fnode_dict
> {'pipe:[19040]’: ['2497', '2498']} 
```

This dictionary is then passed to a graph generator, which generates the complex network graph of all IPCs depicting their inter-connection.
