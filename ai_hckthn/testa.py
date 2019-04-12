import os, uuid, sys, time, subprocess
from azure.storage.blob import BlockBlobService, PublicAccess

import json
import requests
import numpy as np
import time

# login and create the local blob control object...
# must run this first
# Create the BlockBlockService that is used to call the Blob service for the storage account
def def_credentials(acc_key):
    try:
        global block_blob_service 
        block_blob_service = BlockBlobService(account_name='studyhack', account_key=acc_key)
    except Exception as e:
        print(e)

# Upload file, use local_file_name for the blob name
def blob_upload(container_name, local_file_name, full_path_to_file):    
    try:
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
    except Exception as e:
        print(e)

def upload(path, server_path):
    pass
    # upload the files 

# Create a container called 'quickstartblobs'
def create_cont(container_name):        
    try:
        block_blob_service.create_container(container_name)
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    except Exception as e:
        print(e)


# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
def_credentials('g0X13X1yu1h7sE0c/Hu6DR88b1J+MqIKqVteexoc82SUsVBdwl6dNzaaNUXZRfVCcXWUYs1qC4/nx1hO+lS6Iw==')
# START

dt_string = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
audio_container = dt_string+'-audio'
image_container = dt_string+'-image'

create_cont(audio_container)
create_cont(image_container)

dt_string = time.strftime('%Y%m%d-%H%M%S', time.gmtime())

count = 0
prev_loop_time = time.time()
while True:
    if count%2:
        wavName = 'A.wav'
        imgName = 'A.png'
        wavUpload = 'B.wav'
        imgUpload = 'B.png'
    else:
        wavName = 'B.wav'
        imgName = 'B.png'
        wavUpload = 'A.wav'
        imgUpload = 'A.png'

    pirecord = subprocess.Popen(['arecord -f S16_LE -c2 -r 44100  -d 10 {}'.format(wavName)], shell=True)
    picamera = subprocess.Popen(["raspistill -o {}".format(imgName)],shell=True)
    
    if count != 0:
        blob_upload(audio_container, dt_string+'.wav', wavUpload)
        blob_upload(image_container, dt_string+'.png', imgUpload)

    start = time.time()
    while pirecord.poll() == None:
        pass

    pirecord.kill()

    while picamera.poll() == None:
        pass
    picamera.kill()
    # upload()

    count += 1
    dt_string = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
    print('dt_string ', dt_string)
    print('Time of loop ', prev_loop_time - time.time())
    prev_loop_time = time.time()

