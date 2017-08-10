from oauth2client.client import GoogleCredentials
from google.cloud import vision
from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings
from string import upper, replace
import matplotlib.pyplot as plt
import csv
import json
from os import listdir
from os.path import isfile,join

############### Uploads Images to Azure Blob storage ###############
''''
Configuration Details for connecting to Azure Data store account 
'''
ACCOUNT_NAME ='iconnectstore'
ACCOUNT_KEY = 'xFHQLfmlzo47eRlHdopzagrATj8m6xiDlGWZ9shAhReFnJy5BjHf5gE86H1DcYe7RdqKJWhQ8rblahMZlRcDgA=='
CONTAINER_NAME = 'imagecontainer'
IMAGE_DIRECTORY = 'C://Users//acrotrend9//Desktop//pics//'
IMAGE_DIRECTORY_DOWNLOAD = 'C://Users//acrotrend9//Desktop//pics_dwnld//'

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

##############################Download Images from Azure Data Store to Local Directory################################################################


generator = block_blob_service.list_blobs(CONTAINER_NAME)
for blob in generator:
    print(blob.name)
    block_blob_service.get_blob_to_path(CONTAINER_NAME, blob.name,join(IMAGE_DIRECTORY_DOWNLOAD,blob.name ))


##################################Run Vision API over the Images##########################################################################
columns = ["Image Name","Joy", "Anger", "Surprised", "Sorrow","Confidence","No_of_faces"]


'''
csv file path for storing analysis result from Vision API
'''
open_file = open('C:\\Users\\acrotrend9\\Desktop\\files\\image_metadata.csv','w')
csv_file = csv.writer(open_file)
csv_file.writerow(columns)

'''
Set Google cloud enviornment
'''
credentials = GoogleCredentials.get_application_default()

'''
Set Project id 
'''
client = vision.Client(project='reseacrh-173507')

'''
Get list of files from Local Directory for Image Analaysis
'''
local_file_list = [f for f in listdir(IMAGE_DIRECTORY_DOWNLOAD) if isfile(join(IMAGE_DIRECTORY_DOWNLOAD, f))]
print(local_file_list)

no_of_files = len(local_file_list)
for i in range(no_of_files):
    local_file = join(IMAGE_DIRECTORY_DOWNLOAD, local_file_list[i])
    image = client.image(filename=join(IMAGE_DIRECTORY_DOWNLOAD, local_file_list[i]))
    image_name = local_file_list[i]
    faces = image.detect_faces(limit=10)
    labels = image.detect_labels(limit=15)
    no_of_faces = len(faces)
    try:
        for face in faces :
            print "Sentiment Analysis For Face \n"
            emotions_list = [image_name,face.joy,face.anger,face.surprise,face.sorrow,round(face.detection_confidence *100,2),no_of_faces]
            print (emotions_list)
            csv_file.writerow(emotions_list)
    except:
        print "Something wrong happened when uploading the data %s"%image_name

####################################################################################################################################
'''
for face in faces :
    print "Sentiment Analysis For Face \n"
    #writer.writerow({face.joy,face.anger,face.surprise,face.sorrow,face.detection_confidence*100})
    emotions_list = [face.joy,face.anger,face.surprise,face.sorrow,round(face.detection_confidence *100,2),no_of_faces]
    print (emotions_list)
    csv_file.writerow(emotions_list)
            
print "Labels \t Confidence Score  \n" 
for label in labels :
    print upper(label.description)," \t" ,round(label.score * 100,2) , "%" 
'''