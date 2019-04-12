import time

prevTime = time.time()
while True:
    if time.time() - prevTime > 2:
        prevTime = time.time()
        print('test2 TIME ELAPSED')
        