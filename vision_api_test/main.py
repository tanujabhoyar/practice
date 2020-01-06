# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('Hello, World!')
        self.response.write(self.validate())

    def validate(self):
        import io
        import os

        import time

        # Imports the Google Cloud client library
        # from google.cloud import vision

        from apiclient import discovery
        from oauth2client.client import GoogleCredentials
        # from oauth2client import client

        ANIMAL_OBJECT_CONFIDENCE_SCORE = 0.75
        PERSON_OBJECT_CONFIDENCE_SCORE = 0.50
        GENDER_OBJECT_CONFIDENCE_SCORE = 0.50
        FACE_DETECTION_CONFIDENCE_SCORE = 0.75

        def get_vision_svc():
            """Builds the Vision API service object."""
            credentials = GoogleCredentials.get_application_default()
            oauth_scope = ['https://www.googleapis.com/auth/cloud-vision',
                           'https://www.googleapis.com/auth/cloud-platform']
            scope_cred = credentials.create_scoped(oauth_scope)
            token = scope_cred.get_access_token().access_token
            # http = oauth2_decorator.credentials.authorize(oauth2_decorator.http())
            # vision_svc =  discovery.build('vision','v1', http=http)
            vision_svc = discovery.build('vision', 'v1', credentials=credentials)
            return vision_svc, token

        def validate():
            # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/tanuja/Downloads/tanuja-trial-70955c766f92.json'

            # Instantiates a client
            # client = vision.ImageAnnotatorClient()

            # local image file
            profile_image = 'one student.jpg'
            # # profile_image = image_path

            # with open(profile_image, 'rb') as image_file:
            #     content = image_file.read()
            # Import the base64 encoding library.
            import base64

            # Pass the image data to an encoding function.
            def encode_image(image_file):
                with open(image_file, 'rb') as image_file:
                    image_content = image_file.read()
                return base64.b64encode(image_content)

            vision_svc, token = get_vision_svc()

            request_dict = [{
                'image': {
                    'content': encode_image(profile_image),
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10,
                }],
            }]

            api_request = vision_svc.images().annotate(body={
                'requests': request_dict
            })
            response = api_request.execute()
            labels = []
            print response

            if 'labelAnnotations' in response['responses'][0]:
                labels = response['responses'][0]['labelAnnotations']

            print labels
            # image = vision.types.Image(content=content)

            # remote image file
            # image_uri = 'https://www2.physics.ox.ac.uk/sites/default/files/images/Stan1.jpg'

            # image = vision.types.Image()
            # image.source.image_uri = image_uri

            # objects = client.object_localization(
            #     image=image).localized_object_annotations
            #
            # print('Number of objects found: {}'.format(len(objects)))
            # persons = []
            # object_list = [(object_.name, object_.score) for object_ in objects]
            # taglist = [object_.name for object_ in objects]
            # if 'Animal' in taglist or 'Cat' in taglist or 'Dog' in taglist:
            #     print "inside animal loop"
            #     for object_ in objects:
            #         if object_.name in ('Animal', 'Cat', 'Dog') and object_.score >= ANIMAL_OBJECT_CONFIDENCE_SCORE:
            #             return "not a valid picture, pet, animal in picture"
            # if 'Person' not in taglist:
            #     for object_ in objects:
            #         if object_.name in ('Man', 'Woman') and object_.score >= GENDER_OBJECT_CONFIDENCE_SCORE:
            #             persons.append((object_.name, object_.score))
            # else:
            #     for object_ in objects:
            #         if object_.name == 'Person' and object_.score >= PERSON_OBJECT_CONFIDENCE_SCORE:
            #             persons.append((object_.name, object_.score))
            # print object_list
            # if persons:
            #     if len(persons) > 1:
            #         return "not a valid picture more than one person in picture"
            #     response = client.face_detection(image=image)
            #     faces = response.face_annotations
            #     likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
            #                        'LIKELY', 'VERY_LIKELY')
            #
            #     if not faces:
            #         return "not valid picture no face detected"
            #     else:
            #         if len(faces) > 1:
            #             return "not valid picture more than one face detected"
            #         face = faces[0]
            #         print face.blurred_likelihood
            #         if likelihood_name[face.blurred_likelihood] in ('LIKELY', 'VERY_LIKELY'):
            #             return "not valid picture picture is blurred"
            #         print face.detection_confidence
            #         if face.detection_confidence >= FACE_DETECTION_CONFIDENCE_SCORE:  # should be 75
            #             return "valid profile"
            #         else:
            #             return "not valid as face detection confidence is less than 75"
            #
            # else:
            #     return "not valid picture no person detected"


if __name__ == '__main__':
    # image = '/home/tanuja/Desktop/profile1.jpeg'
    # image = '/home/tanuja/Desktop/oneboy.jpeg' # was not able to detect face
    print validate()


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

