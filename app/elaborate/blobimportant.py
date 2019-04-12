from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccessls -lencd 
from azure.storage.blob import ContentSettings

def credentials():
    block_blob_service = BlockBlobService(account_name='studyhack', account_key='g0X13X1yu1h7sE0c/Hu6DR88b1J+MqIKqVteexoc82SUsVBdwl6dNzaaNUXZRfVCcXWUYs1qC4/nx1hO+lS6Iw==')

def ccont():
    block_blob_service.create_container('ex1', public_access=PublicAccess.Container)

def lblob
    block_blob_service.create_blob_from_path(
        'mycontainer',
        'myblockblob',
        'sunset.png',
        content_settings=ContentSettings(content_type='image/png')
        generator = block_blob_service.list_blobs('mycontainer')
            for blob in generator:
    	        print(blob.name)
