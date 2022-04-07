""" Download ProfileImage from URL and store in s3
    as full and thumbnail size.

   This program does 
   - Gets triggered by SNS 
   - Gets message data from Sns event
   - create image in two size for full and thumbnail view
   - stores both the images in private/id directory in designated bucket
   - logs the data in between operations

    author: ashraf minhaj
    mail  : ashraf_minhaj@yahoo.com
"""


import io
import json
import boto3
import logging
import requests
import configparser
from PIL import Image

# initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_data_from_sns(event):
    """ get RecommendeeExpertId CandidateProfileImage and return as url and id """
    logger.info('Getting ID and ImageURL from SNS message')
    logger.info(type(event))
    
    message = event['Records'][0]['Sns']['Message']  # gets message string
    logger.info('Type of message')                    
    logger.info(type(message))                       # log type of received message
    
    logger.info('Convert str message to dict')
    parsed_message = json.loads(message)             # convert into dict
    logger.info(type(parsed_message))
    
    # getting candidate id and image url
    logger.info('Getting the data we needed')
    id = parsed_message['RecommendationData']['RecommendeeExpertId']
    url = parsed_message['RecommendationData']['CandidateProfileImage']
    logger.info(id)
    logger.info(url)
    logger.info('SNS data extraction successful')
    return id, url


def get_response(url):
    """ make a get request """
    return requests.get(url)


def get_images(source, th_w, th_h):
    """ returns profile full and thumbanil image."""
    logger.info('Getting Images')
    full_img      = Image.open(io.BytesIO(source.content))
    thumbnail_img = full_img.resize((int(th_w), int(th_h)), Image.ANTIALIAS)

    # after resizing PIL image format changes, so we need this part
    # instead of storing in file, we are storing in memory
    b = io.BytesIO()
    thumbnail_img.save(b,format="jpeg")
    thumbnail_img = Image.open(b)

    logger.info('Got images')
    return full_img, thumbnail_img


def store(img, path, client, bucket):
    """ given image, image path, client object and target bucket
    this stores image into destined s3 bucket. """
    logger.info('Writing img.')
    temp_file = io.BytesIO()
    img.save(temp_file, format=img.format)
    temp_file.seek(0)
    client.upload_fileobj(temp_file, bucket, path)


def image_downloader(event, context):
    # log 
    logger.info('Starting Downloader.')
    
    # read config files first
    logger.info('Reading Config/Environment Variable')
    config = configparser.ConfigParser()
    config.read('config.ini')

    config_data        = config['default']
    directory          = config_data['dir']
    target_bucket      = config_data['bucket']
    full_img_name      = config_data['full_img_name']
    thumbnail_img_name = config_data['thumbnail_img_name']
    thumbnail_w        = config_data['thumbnail_w']
    thumbnail_h        = config_data['thumbnail_h']
    image_extension    = config_data['image_extension']

    # get data from sns msg
    logger.info('Getting data from sns.')
    id, image_url = get_data_from_sns(event)

    # make a get request to get image
    logger.info('Getting image from url.')
    response = get_response(image_url)
    logger.info(response.status_code)

    # prepare images
    logger.info('Prepare images.')
    full_img, thumbnail_img = get_images(response, thumbnail_w, thumbnail_h)
    
    full_img_path       = f'{directory}/{id}/{full_img_name}.{image_extension}'
    thumbnail_img_path  = f'{directory}/{id}/{thumbnail_img_name}.{image_extension}'

    logger.info('Writing on s3')
    s3 = boto3.client('s3')
    store(full_img, full_img_path, s3, target_bucket)
    store(thumbnail_img, thumbnail_img_path, s3, target_bucket)

    # finally log that it was a success
    output_text = f'Images stored in {target_bucket} for id: {id}'
    logger.info(output_text)
    return output_text