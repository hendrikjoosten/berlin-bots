import os, uuid, sys, time, subprocess
from azure.storage.blob import BlockBlobService, PublicAccess

import json
import requests
import numpy as np
import time

AUDIO_INTERVAL = 15 # seconds
IMAGE_INTERVAL = 10

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
# For blob storage
def_credentials('g0X13X1yu1h7sE0c/Hu6DR88b1J+MqIKqVteexoc82SUsVBdwl6dNzaaNUXZRfVCcXWUYs1qC4/nx1hO+lS6Iw==')

# START

# CREATE CONTAINERS FOR THE SESSION
dt_string = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
audio_container = dt_string+'-audio'
image_container = dt_string+'-image'

print('Audio container for this session: {}'.format(audio_container))
print('Image container for this session: {}'.format(image_container))

create_cont(audio_container)
create_cont(image_container)

# INIT LOOP VARIABLES
audio_count = 0
audio_name = ''
audio_time = 0
audio_gmtime = time.gmtime()
audio_proc = subprocess.Popen(['echo', 'start'])

image_count = 0
image_name = ''
image_time = 0
image_gmtime = time.gmtime()
image_proc = subprocess.Popen(['echo', 'start'])

while True:
    now = time.time()
    
    if audio_proc.poll() != None:
        # Recording audio done!
        audio_proc.kill()
        # Save details for later
        audio_uploadName = audio_name # previously used name on Pi
        audio_timeDif = now - audio_time
        audio_serverName = time.strftime('%Y%m%d-%H%M%S.wav', audio_gmtime)
        # Start recording the next
        audio_name = '{}.wav'.format('B' if audio_count%2 else 'A')
        audio_time = now
        audio_gmtime = time.gmtime()
        audio_proc = subprocess.Popen(['arecord', '-f','S16_LE', '-c2', '-r','44100',  '-d', '{}'.format(AUDIO_INTERVAL), '{}'.format(audio_name)], shell=False)

        if audio_count != 0:
            # Upload the previous
            blob_upload(audio_container, audio_serverName, audio_uploadName)
            print('Audio {:4} done. {} {:6.3f} s'.format(audio_count, audio_serverName, audio_timeDif))
        audio_count = audio_count + 1

    
    if (image_proc.poll() != None) and (now - image_time >= IMAGE_INTERVAL):
        # Taking image done!
        image_proc.kill()
        # Save details for later
        image_uploadName = image_name # previously used name on Pi
        image_timeDif = now - image_time
        image_serverName = time.strftime('%Y%m%d-%H%M%S.jpg', image_gmtime)
        # Start recording the next
        image_name = '{}.wav'.format('B' if image_count%2 else 'A')
        image_time = now
        image_gmtime = time.gmtime()
        image_proc = subprocess.Popen(["raspistill -o {}".format(image_name)],shell=True)

        if image_count != 0:
            # Upload the previous
            blob_upload(image_container, image_serverName, image_uploadName)
            print('Image {:4} done. {} {:6.3f} s'.format(image_count, image_serverName, image_timeDif))
        image_count = image_count + 1

    time.sleep(0.002) # Reduces processor usage
