
import subprocess
import sys
import time

#proc = subprocess.Popen([sys.executable, 'test.py'], -1, None, None, sys.stdout, sys.stderr, None, 0, True)
proc = subprocess.Popen([sys.executable, 'test.py'], shell=True)
print('test.py was run')

proc2 = subprocess.Popen([sys.executable, 'test2.py'], shell=True)
print('test2.py was run')

start = time.time()
while time.time() - start < 5:
    pass

proc.kill()
proc2.kill()

