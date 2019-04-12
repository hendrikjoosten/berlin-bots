import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess


def def_credentials(acc_key):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='studyhack', account_key=acc_key)
    except Exception as e:
        print(e)


def create_cont():        
    try:
        # Create a container called 'quickstartblobs'.
        container_name ='quickstartblobs'
        block_blob_service.create_container(container_name)
        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    except Exception as e:
        print(e)


def create_local():    
    try:
        # Create a file in Documents to test the upload and download.
        local_path=os.path.expanduser("~/Documents")
        local_file_name ="QuickStart_" + str(uuid.uuid4()) + ".txt"
        full_path_to_file =os.path.join(local_path, local_file_name)
    except Exception as e:
        print(e)

def create_local_text():    
    try:
        # Write text to the file.
        file = open(full_path_to_file,  'w')
        file.write("Hello, World!")
        file.close()
    except Exception as e:
        print(e)
    
def create_bbs():        
    try:
        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)
    except Exception as e:
        print(e)


def blob_uplaod():    
    try:
        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
    except Exception as e:
        print(e)

def blob_list():    
    try:
        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
    except Exception as e:
        print(e)

def blob_download():    
    try:
        # Download the blob(s).
        # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
        full_path_to_file2 = os.path.join(local_path, str.replace(local_file_name ,'.txt', '_DOWNLOADED.txt'))
        print("\nDownloading blob to " + full_path_to_file2)
        block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)
    except Exception as e:
        print(e)





