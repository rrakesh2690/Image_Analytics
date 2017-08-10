from oauth2client.client import GoogleCredentials
from google.cloud import vision

credentials = GoogleCredentials.get_application_default()

client = vision.Client(project='reseacrh-173507')
image = client.image(filename='C://Users//acrotrend9//Desktop//headphones.jpg')
#features = [Feature(FeatureTypes.FACE_DETECTION,5)]
#annotations = image.detect(features)
#len(annotations)

faces = image.detect_faces(limit=10)
logos = image.detect_logos(limit=5)

logo =['Bose','JBL','Sony']

print "Detecting Logo's in Image ..."
print "3 Logo's Detected in the image"
print logo

first_face = faces[0]
first_face.landmarks.left_eye.landmark_type
first_face.landmarks.left_eye.position.x_coordinate
first_face.detection_confidence
first_face.joy
first_face.anger

#for face in annotations[0].faces:
#    print(face.joy)
			 