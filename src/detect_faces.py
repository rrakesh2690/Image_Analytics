"""Draws squares around detected faces in the given image."""
from oauth2client.client import GoogleCredentials
import argparse
from google.cloud import vision
from azure.storage.blob import BlockBlobService 
from azure.storage.file import FileService
from azure.storage.blob import ContentSettings
from PIL import Image, ImageDraw
import csv
import os 
from os.path import isfile,join
from os import listdir

'''
Set Google cloud enviornment
'''
credentials = GoogleCredentials.get_application_default()
client = vision.Client(project='reseacrh-173507')

############### Uploads Images to Azure Blob storage ###############
''''
Configuration Details for connecting to Azure Data store account 
'''
ACCOUNT_NAME ='iconnectstore'
ACCOUNT_KEY = 'xFHQLfmlzo47eRlHdopzagrATj8m6xiDlGWZ9shAhReFnJy5BjHf5gE86H1DcYe7RdqKJWhQ8rblahMZlRcDgA=='
CONTAINER_NAME = 'imagecontainer'
IMAGE_DIRECTORY = 'C://Users//acrotrend9//Desktop//pics//'
IMAGE_DIRECTORY_DOWNLOAD = 'C://Users//acrotrend9//Desktop//pics_dwnld//'
FILE_SHARE_NAME = 'imagemetadata'


'''
Configure azure storage account for the session 
'''
block_blob_service = BlockBlobService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

file_service = FileService(account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)


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

'''
Function to detect face in the pictures
'''
def detect_face(face_file, max_results=10):
    """Uses the Vision API to detect faces in the given file.
    Args:
        face_file: A file-like object containing an image with faces.
    Returns:
        An array of Face objects with information about the picture.
    """
    content = face_file.read()
    # [START get_vision_service]
    image = vision.Client(project='reseacrh-173507').image(content=content)
    # [END get_vision_service]
    return image.detect_faces()
 
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.
    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(bound.x_coordinate, bound.y_coordinate)
               for bound in face.bounds.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)

def detect_emotion(IMAGE_DIRECTORY_DOWNLOAD,metadata_file):
    
    """Stores the sentiment information for each face in image to a csv file 
    Args:
      IMAGE_DIRECTORY_DOWNLOAD: a file containing the image with the faces.
      metadata_file: the name of the csv file to be created, where the
      sentiment information for each face in image will be stored alongwith confidence score.   
    """
    #columns = ["Image Name","Joy", "Anger", "Surprised", "Sorrow","Confidence","No_of_faces"]
    open_file = open(metadata_file,'a')
    csv_file = csv.writer(open_file)
    #csv_file.writerow(columns)
    #local_file_list = [f for f in listdir(IMAGE_DIRECTORY_DOWNLOAD) if isfile(join(IMAGE_DIRECTORY_DOWNLOAD, f))]
    #print(local_file_list)
    #no_of_files = len(local_file_list)
    #for i in range(no_of_files):
    #    local_file = join(IMAGE_DIRECTORY_DOWNLOAD, local_file_list[i])
    image = client.image(filename=IMAGE_DIRECTORY_DOWNLOAD)
    image_name = os.path.basename(IMAGE_DIRECTORY_DOWNLOAD)
    faces = image.detect_faces(limit=10)
    #    labels = image.detect_labels(limit=15)
    no_of_faces = len(faces)
    #try:
    for face in faces :
            print "Sentiment Analysis For Face \n"
            emotions_list = [image_name,face.joy,face.anger,face.surprise,face.sorrow,round(face.detection_confidence *100,2),no_of_faces]
            print (emotions_list)
            csv_file.writerow(emotions_list)
    #except:
    #    print "Something wrong happened when uploading the data %s"%image_name

def main(input_filename, output_filename, max_results,metadata_img):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)
        detect_emotion(input_filename,metadata_img )
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects faces in the given image.')
    parser.add_argument(
        'input_image', help='the image you\'d like to detect faces in.')
    parser.add_argument(
        '--out', dest='output', default='out.jpg',
        help='the name of the output file.')
    parser.add_argument(
        '--max-results', dest='max_results', default=4,
        help='the max results of face detection.')
    parser.add_argument(
        '--meta-data', dest='metadata_csv', default='out.jpg',
        help='the name of the image Analysis file.')
    args = parser.parse_args()
    
    local_file_list = [f for f in listdir(args.input_image) if isfile(join(args.input_image, f))]
    print(local_file_list)
    no_of_files = len(local_file_list)
    for i in range(no_of_files):
        local_file = join(args.input_image, local_file_list[i])
        image = client.image(filename=join(args.input_image, local_file_list[i]))
        image_name = local_file_list[i]
        output_image = join(args.output,image_name)
        main(local_file, output_image, args.max_results,args.metadata_csv)
         
    out_file_name = os.path.basename(args.metadata_csv)
    local_file_name = args.metadata_csv
    block_blob_service.create_blob_from_path(FILE_SHARE_NAME, out_file_name, local_file_name,content_settings=ContentSettings(content_type='application/csv'))
    