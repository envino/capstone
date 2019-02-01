from __future__ import print_function

import boto3
import decimal
import json
from urllib.parse import unquote
import datetime
import time
from boto3.dynamodb.conditions import Key, Attr

print('Loading function')

s3 = boto3.client('s3')
resource = boto3.resource('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')

dynamodbr = boto3.resource('dynamodb')
doortable = dynamodbr.Table('latestentry')



# --------------- Helper Functions to call Rekognition APIs ------------------

#if (Confidence > 95%):
#def detect_faces(bucket, key):
 #   response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
  #  return response

	
# --------------- Main handler ------------------

#bucket = s3.get_object(Bucket='myownshoehomies', Key='IMG_3802.JPG')


#detect_faces(bucket, key)


def lambda_handler(event, context):

#if __name__ == "__main__":

	bucket_name = event['Records'][0]['s3']['bucket']['name']
	collectionId='trusted'
	fileName = event['Records'][0]['s3']['object']['key']

	
	response = rekognition.detect_faces(Image={'S3Object':{'Bucket':bucket_name,'Name':fileName}},Attributes=['DEFAULT'])	
	#need error clause
	if response['FaceDetails'] == []:
		print('No Face Detected')
	else:

	
		for detail in response['FaceDetails']:
			value = detail['Confidence']
			detail['Confidence'] = decimal.Decimal(value)
			labeled = detail['Confidence']
		

	
		if labeled >= 95:
			index=rekognition.search_faces_by_image(CollectionId=collectionId, Image={'S3Object':{'Bucket':bucket_name,'Name':fileName}})

			#enriching the rekognition labels
			facenone = index['FaceMatches']
			if facenone == []:
				value = "UNKNOWN"
				value = str(value)
				response = doortable.put_item(Item = {'entry': 1, 'time': fileName, 'faceId': value})
				
			else:
				faceId = index['FaceMatches'][0]['Face']['FaceId']
				faceId = str(faceId)
				conf = index['FaceMatches'][0]['Similarity']
				conf = decimal.Decimal(conf)
				response = doortable.put_item(Item = {'entry': 1, 'time': fileName, 'faceId': faceId, 'Confidence': conf})

