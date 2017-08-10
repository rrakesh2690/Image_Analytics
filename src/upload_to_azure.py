from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings
from os import listdir
from os.path import isfile,join

ACCOUNT_NAME ='iconnectstore'
ACCOUNT_KEY = 'xFHQLfmlzo47eRlHdopzagrATj8m6xiDlGWZ9shAhReFnJy5BjHf5gE86H1DcYe7RdqKJWhQ8rblahMZlRcDgA=='
CONTAINER_NAME = 'imagecontainer'
IMAGE_DIRECTORY = 'C://Users//acrotrend9//Desktop//pics//'

'''
Configure azure storage account for the session 
'''
block_blob_service = BlockBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

'''
Create Container if required or comment out 
'''
block_blob_service.create_container(CONTAINER_NAME)

'''
Find all files in the Local Image Directory (excluding directory)
'''
local_file_list = [f for f in listdir(IMAGE_DIRECTORY) if isfile(join(IMAGE_DIRECTORY, f))]
print(local_file_list)

#Upload the CSV file to Azure cloud
no_of_files = len(local_file_list)
for i in range(no_of_files):
    local_file = join(IMAGE_DIRECTORY, local_file_list[i])
    blob_name = local_file_list[i]
    try:
        block_blob_service.create_blob_from_path(CONTAINER_NAME, blob_name, local_file,content_settings=ContentSettings(content_type='image/jpg'))
    except:
        print "something wrong happened when uploading the data %s"%blob_name

'''
# Check the list of blob
generator = block_blob_service.list_blobs('blobdump')
for blob in generator:
    print(blob.name)

# Download file From Azure storage
block_blob_service.get_blob_to_path('blobdump', 'Madhav.jpg', 'out_madhav.jpg')
'''