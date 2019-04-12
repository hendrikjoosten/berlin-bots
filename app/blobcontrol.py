# IN MICROSOFT TALK
# container = folder
# blob = file

# REMEMBER TO INSTALL THE MODULES IN THE REQUIREMENTS.TXT
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess


# login and create the local blob control object...
# must run this first
# Create the BlockBlockService that is used to call the Blob service for the storage account
def def_credentials(acc_key):
    try:
        global block_blob_service 
        block_blob_service = BlockBlobService(account_name='studyhack', account_key=acc_key)
    except Exception as e:
        print(e)


# Create a container called 'quickstartblobs'
def create_cont(container_name):        
    try:
        block_blob_service.create_container(container_name)
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    except Exception as e:
        print(e)


# Upload file, use local_file_name for the blob name
def blob_uplaod(container_name, local_file_name, full_path_to_file):    
    try:
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
    except Exception as e:
        print(e)


# List the blobs in the container
def blob_list(container_name):    
    try:
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
    except Exception as e:
        print(e)

# Download the blob(s).
# Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
def blob_download(container_name, local_file_name, local_path):    
    try:
        full_path_to_file2 = os.path.join(local_path, local_file_name)
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)
    except Exception as e:
        print(e)





