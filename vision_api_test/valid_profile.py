import io
import os

import time

# Imports the Google Cloud client library
from google.cloud import vision


def validate():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    # local image file
    # profile_image = '/home/tanuja/Desktop/profile1.jpeg'
    # profile_image = image_path
    # with open(profile_image, 'rb') as image_file:
    #     content = image_file.read()
    # image = vision.types.Image(content=content)

    # remote image file
    image_uri = 'https://www2.physics.ox.ac.uk/sites/default/files/images/Stan1.jpg'

    image = vision.types.Image()
    image.source.image_uri = image_uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    persons = []
    object_list = [(object_.name, object_.score) for object_ in objects]
    taglist = [object_.name for object_ in objects]
    if 'Person' not in taglist:
        for object_ in objects:
            if object_.name in ('Man', 'Woman') and object_.score >= 0.50:
                persons.append((object_.name, object_.score))
    else:
        for object_ in objects:
            if object_.name == 'Person' and object_.score >= 0.50:
                persons.append((object_.name, object_.score))
    print object_list
    if persons:
        if len(persons) > 1:
            return "not a valid picture more than one person in picture"
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
            print face.blurred_likelihood
            if likelihood_name[face.blurred_likelihood] in ('LIKELY', 'VERY_LIKELY'):
                return "not valid picture picture is blurred"
            print face.detection_confidence
            if face.detection_confidence >= 0.75: # should be 75
                return "valid profile"
            else:
                return "not valid as face detection confidence is less than 75"

    else:
        return "not valid picture no person detected"


if __name__ == '__main__':
    # image = '/home/tanuja/Desktop/profile1.jpeg'
    # image = '/home/tanuja/Desktop/oneboy.jpeg' # was not able to detect face
    print validate()
