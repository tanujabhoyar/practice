import io
import os

import time


from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# Import the base64 encoding library.
import base64


ANIMAL_OBJECT_CONFIDENCE_SCORE = 0.75
PERSON_OBJECT_CONFIDENCE_SCORE = 0.50
GENDER_OBJECT_CONFIDENCE_SCORE = 0.50
FACE_DETECTION_CONFIDENCE_SCORE = 0.75


# Pass the image data to an encoding function.
def encode_image(image_file):
    with open(image_file, 'rb') as image_file:
        image_content = image_file.read()
    return base64.b64encode(image_content)


def get_vision_svc():
    """Builds the Vision API service object."""
    credentials = GoogleCredentials.get_application_default()
    vision_svc = discovery.build('vision', 'v1', credentials=credentials)
    return vision_svc


def validate():
    # start_time = time.time()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/tanuja/Downloads/tanuja-trial-70955c766f92.json'


    # local image file
    # profile_image = '/home/tanuja/Desktop/not_valid_1.jpeg'
    image_name = 'personwithpet.jpeg'
    profile_image = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', image_name)
    profile_image = '/home/tanuja/Downloads/PHOTOS/GOOD_PHOTOS/STSEP191093491_photo_old.jpeg'
    request_dict = [{
        'image': {
            'content': encode_image(profile_image),
        },
        'features': [{
                'type': 'OBJECT_LOCALIZATION',
                'maxResults': 10,
             },
            {
                'type': 'FACE_DETECTION',
                'maxResults': 10,
            }
        ]
    }]


    # remote image file
    # image_uri = 'https://www2.physics.ox.ac.uk/sites/default/files/images/Stan1.jpg'

    vision_svc = get_vision_svc()
    api_request = vision_svc.images().annotate(body={
        'requests': request_dict
    })
    response = api_request.execute()
    objects = []
    # print response

    if 'localizedObjectAnnotations' in response['responses'][0]:
        objects = response['responses'][0]['localizedObjectAnnotations']

    # print objects
    # print('Number of objects found: {}'.format(len(objects)))
    persons = []
    object_list = [(object_['name'], object_['score']) for object_ in objects]
    taglist = [object_['name'] for object_ in objects]
    if 'Animal' in taglist or 'Cat' in taglist or 'Dog' in taglist:
        # print "inside animal loop"
        for object_ in objects:
            if object_['name'] in ('Animal', 'Cat', 'Dog') and object_['score'] >= ANIMAL_OBJECT_CONFIDENCE_SCORE:
                return "not a valid picture, pet, animal in picture"
    if 'Person' not in taglist:
        for object_ in objects:
            if object_['name'] in ('Man', 'Woman') and object_['score'] >= GENDER_OBJECT_CONFIDENCE_SCORE:
                persons.append((object_['name'], object_['score']))
    else:
        for object_ in objects:
            if object_['name'] == 'Person' and object_['score'] >= PERSON_OBJECT_CONFIDENCE_SCORE:
                persons.append((object_['name'], object_['score']))
    # print object_list
    if persons:
        if len(persons) > 1:
            return "not a valid picture more than one person in picture"
        faces = []
        if 'faceAnnotations' in response['responses'][0]:
            faces = response['responses'][0]['faceAnnotations']
        if not faces:
            return "not valid picture no face detected"
        else:
            if len(faces) > 1:
                return "not valid picture more than one face detected"
            face = faces[0]
            if face['blurredLikelihood'] in ('LIKELY', 'VERY_LIKELY'):
                return "not valid picture picture is blurred"
            # print face['detectionConfidence']
            if face['detectionConfidence'] >= FACE_DETECTION_CONFIDENCE_SCORE:  # should be 75
                return "valid profile"
            else:
                return "not valid as face detection confidence is less than 75"
    else:
        return "not valid picture no person detected"


if __name__ == '__main__':
    start_time = time.time()
    print validate()
    time_taken = time.time() - start_time
    print "time taken ", time_taken



