# Python Interprocess Communication examples
Some examples of interprocess communication connecting different python versions

## Named Pipes (FIFO)
Python2 and Python3 both are running independently from each other, opening the pipes to perform read and write.

Requirements:
- independent execution of both sides
- shared path string where to find the pipes in the filesystem

Run: `python3 python3.py`

Run: `python2 python2.py`

## Subprocess Pipes
Python2 creats an anonymous (unnamed) pipe and then starts Python3 as subprocess with the pipe as parameter.

Requirements:
- execution only of python2

Run: `python2 subprocess.py`