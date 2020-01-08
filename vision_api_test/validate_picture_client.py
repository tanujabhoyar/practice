import io
import os

import time

# Imports the Google Cloud client library
from google.cloud import vision

ANIMAL_OBJECT_CONFIDENCE_SCORE = 0.75
PERSON_OBJECT_CONFIDENCE_SCORE = 0.50
GENDER_OBJECT_CONFIDENCE_SCORE = 0.50
FACE_DETECTION_CONFIDENCE_SCORE = 0.75
MIN_AREA_COVERAGE_BY_PERSON_OBJECT = 0.50


def validate(image_path=None):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/tanuja/Downloads/tanuja-trial-70955c766f92.json'

    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    # local image file
    # image_name = 'not_valid_1.jpeg'
    # profile_image = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', image_name)
    # profile_image = '/home/tanuja/Downloads/PHOTOS/GOOD_PHOTOS/STSEP191093491_photo_old.jpeg'
    profile_image = image_path
    with open(profile_image, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    # remote image file
    # image_uri = 'https://www2.physics.ox.ac.uk/sites/default/files/images/Stan1.jpg'

    # image = vision.types.Image()
    # image.source.image_uri = image_uri

    objects = client.object_localization(
        image=image).localized_object_annotations


    # print('Number of objects found: {}'.format(len(objects)))
    persons = []
    object_list = [(object_.name, object_.score) for object_ in objects]
    taglist = [object_.name for object_ in objects]
    # print taglist
    if 'Person' not in taglist:
        for object_ in objects:
            if object_.name in ('Man', 'Woman') and object_.score >= GENDER_OBJECT_CONFIDENCE_SCORE:
                persons.append((object_.name, object_.bounding_poly))
    else:
        for object_ in objects:
            if object_.name == 'Person' and object_.score >= PERSON_OBJECT_CONFIDENCE_SCORE:
                persons.append((object_.name, object_.bounding_poly))

    if persons:
        if len(persons) > 1:
            return "not a valid picture more than one person in picture"
        if 'Animal' in taglist or 'Cat' in taglist or 'Dog' in taglist:
            for object_ in objects:
                if object_.name in ('Animal', 'Cat', 'Dog') and object_.score >= ANIMAL_OBJECT_CONFIDENCE_SCORE:
                    return "not a valid picture, pet, animal in picture"
        vertices = persons[0][1].normalized_vertices
        area = (vertices[1].x - vertices[0].x) * (vertices[3].y - vertices[0].y)
        print "area coverred by object:     ", area
        if area < MIN_AREA_COVERAGE_BY_PERSON_OBJECT:
            return "not valid picture image area too small"
        response = client.face_detection(image=image)
        faces = response.face_annotations
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')

        if not faces:
            return "not valid picture no face detected"
        else:
            if len(faces) > 1:
                return "not valid picture more than one face detected"
            face = faces[0]
            # print face.blurred_likelihood
            if likelihood_name[face.blurred_likelihood] in ('LIKELY', 'VERY_LIKELY'):
                return "not valid picture picture is blurred"
            # print face.detection_confidence
            if face.detection_confidence >= FACE_DETECTION_CONFIDENCE_SCORE:  # should be 75
                return "valid profile"
            else:
                return "not valid as face detection confidence is less than 75"

    else:
        if not objects:
            return "not valid image (signature)"
        response = client.label_detection(image=image)
        labels = response.label_annotations
        if labels:
            valid_signature = False
            for label in labels:
                if label.description in ('Text', 'Autograph', 'Signature', 'Handwriting') and label.score >= 0.80:
                    valid_signature = True
                    return "valid signature"
            if not valid_signature:
                return "not valid signature"
        else:
            return "not valid picture no person detected"


if __name__ == '__main__':
    # pictures_folder = '/home/tanuja/Desktop/signatures'
    image_file_path = '/home/tanuja/Desktop/signatures/not_good_signature.jpeg'
    # pictures_folder = '/home/tanuja/Downloads/PHOTOS/GOOD_PHOTOS'
    # pictures_folder = '/home/tanuja/Desktop/profiles'
    # image_file_path = '/home/tanuja/Downloads/PHOTOS/BAD_PHOTOS/STSEP191087595_photo_old.jpeg'
    print validate(image_file_path)
    # for (dirpath, dirnames, filenames) in os.walk(pictures_folder):
    #     for file in filenames:
    #         if '.jpeg' in file or '.png' in file:
    #             image_file = os.path.join(dirpath, file)
    #             print image_file
    #             print "SIZE:    ", (os.stat(image_file).st_size)/1024
    #             start_time = time.time()
    #             print "RESULT:  ", validate(image_file)
    #             time_taken = time.time() - start_time
    #             print "Time Taken:  ", time_taken
    #             print "\n\n"
