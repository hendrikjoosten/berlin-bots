import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

from blobcontrol import *

def_credentials('g0X13X1yu1h7sE0c/Hu6DR88b1J+MqIKqVteexoc82SUsVBdwl6dNzaaNUXZRfVCcXWUYs1qC4/nx1hO+lS6Iw==')

create_cont('yoyoyo4')

blob_uplaod('yoyoyo4','hello.py','/home/wulv/Desktop/github/berlin-bots/app/hello.py')

blob_list('yoyoyo4')

blob_download('yoyoyo4','hello.py','/home/wulv/Desktop/github/berlin-bots/app')
