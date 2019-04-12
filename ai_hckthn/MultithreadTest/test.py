import time

prevTime = time.time()
while True:
    if time.time() - prevTime > 1:
        prevTime = time.time()
        print('test 1_______________')
        