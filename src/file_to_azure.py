'''
This program uploads the processed files with image analysis in csv format to Azure Storgae File Share 
'''

from azure.storage.blob import ContentSettings
from azure.storage.file import FileService
from os import listdir
from os.path import isfile,join

ACCOUNT_NAME ='iconnectstore'
ACCOUNT_KEY = 'xFHQLfmlzo47eRlHdopzagrATj8m6xiDlGWZ9shAhReFnJy5BjHf5gE86H1DcYe7RdqKJWhQ8rblahMZlRcDgA=='
FILE_SHARE_NAME = 'images'
FS_DIRECTORY_NAME = 'iconnectfsd'
LOCAL_FS_DIRECTORY = 'C://Users//acrotrend9//Desktop//files//'

'''
Configure azure storage account for the session 
'''
file_service = FileService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)
file_service.create_share(FILE_SHARE_NAME)

'''
Find all files in the Local Image Directory (excluding directory)
'''
local_file_list = [f for f in listdir(LOCAL_FS_DIRECTORY) if isfile(join(LOCAL_FS_DIRECTORY, f))]
print(local_file_list)

'''
Upload the CSV file to Azure cloud
'''
no_of_files = len(local_file_list)
for i in range(no_of_files):
    local_file = join(LOCAL_FS_DIRECTORY, local_file_list[i])
    file_name = local_file_list[i]
    try:
        file_service.create_file_from_path(FILE_SHARE_NAME,
        None, # We want to create this blob in the root directory, so we specify None for the directory_name
        file_name,
        local_file,
        content_settings=ContentSettings(content_type='application/csv'))
    except:
        print "Something wrong happened when uploading the data %s"%file_name


# Download the CSV file From Azure storage
#block_blob_service.get_blob_to_path('blobdump', 'Madhav.jpg', 'out_madhav.jpg')
