""" Test Image downloader program """

import image_downloader   # the function to test
import unittest
import validators
import json

class ImageDownloaderTest(unittest.TestCase):
    """ This tests the image downloader """
    SNS_MSG = ''

    def test_valid_url(self):
        """ check if candidate_profile_image url is valid """
        # read_sns_message returns recommendee_expert_id and candidate_profile_image
        # we need candidate_profile_image url
        _, url = image_downloader.get_data_from_sns(self.SNS_MSG)     # get candidate_profile_image url
        check_url = validators.url(url)                               # validate url, returns True if ok
        self.assertEqual(check_url, True, 'Invalid URL')

    def test_url_has_img(self):
        """ break the url string and find 'image' word """
        _, url = image_downloader.get_data_from_sns(self.SNS_MSG)     # get candidate_profile_image url
        break_url_string = url.split('/')                             # break the url string by '/'
        image_found = 'image' in break_url_string                     # returns True if 'image' string present
        self.assertEqual(image_found, True, 'No Image info in url')

    def test_get_request_response(self):
        """ check if get_response works """
        _, url = image_downloader.get_data_from_sns(self.SNS_MSG)    # get candidate_profile_image url
        response = image_downloader.get_response(url)                # make the get request
        status = response.status_code                                # get request status code
        self.assertEqual(status, 200, f'request error, stat:{status}')

    def test_image_getter(self):
        """ check if two images are returned """
        _, url = image_downloader.get_data_from_sns(self.SNS_MSG)
        response = image_downloader.get_response(url)
        output = image_downloader.get_images(response, 100, 100)
        num_of_images = len(output)
        print('Got Images:', num_of_images)



# test message
sns_msg = {
    "Records": [
    {
        "EventSource": "aws:sns",
        "EventVersion": "1.0",
        "EventSubscriptionArn": "arn:aws:sns:us-east-1:{{{accountId}}}:ExampleTopic",
        "Sns": {
        "Type": "Notification",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
        "Subject": "example subject",
        "Message": {
            "x": {
            "y": "",
            "name": "kudrot0mia1",
            "z": "https://media-exp1.licdn.com/dms/image/C5603AQFMq1CsrhY_Mw/profile-displayphoto-shrink_200_200/0/1617700314678?e=1640217600&v=beta&t=f_FUwOdfFMw-AY45lEszRWQjTJnK5SgYvT9fwXLcCJ8"
            }
        },
        "Timestamp": "1970-01-01T00:00:00.000Z",
        "SignatureVersion": "1",
        "Signature": "EXAMPLE",
        "SigningCertUrl": "EXAMPLE",
        "UnsubscribeUrl": "EXAMPLE",
        "MessageAttributes": {
            "Test": {
            "Type": "String",
            "Value": "TestString"
            },
            "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
            }
        }
        }
    }
    ]
    }


if __name__ == '__main__':                   # if the code ran
    ImageDownloaderTest.SNS_MSG = json.dumps(sns_msg)    # pass sns_msg
    unittest.main()                          # run test