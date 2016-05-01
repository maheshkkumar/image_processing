# Importing Libraries
import time 
import requests
import cv2
import operator
import numpy as np
import sys

# Variables
_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_key = 'f421a1b3ff16480aa22822d0a5ddc9a4'
_maxNumRetries = 10


class ImageProcessing():

	def __init__(self, url):
		self.urlImage = url

	def get_clould_image_description(self):

		params = { 'visualFeatures' : 'Description'} 
		headers = dict()
		headers['Ocp-Apim-Subscription-Key'] = _key
		headers['Content-Type'] = 'application/json' 
		json = { 'url': self.urlImage } 
		data = None
		result = self.processRequest(json, data, headers, params )
		return result['description']['captions'][0]['text'].encode('UTF8'), [x.encode('UTF8') for x in result['description']['tags']]
		 
	def get_local_image_description(self):
		
		rootUrl = "C:\\Users\\Mahesh Kumar\\Desktop\\"
		pathToFileInDisk = rootUrl+self.urlImage
		with open( pathToFileInDisk, 'rb' ) as f:
				data = f.read()
				
		# Computer Vision parameters
		params = { 'visualFeatures' : 'Description'} 

		headers = dict()
		headers['Ocp-Apim-Subscription-Key'] = _key
		headers['Content-Type'] = 'application/octet-stream'

		json = None

		result = self.processRequest( json, data, headers, params )
		return result['description']['captions'][0]['text'].encode('UTF8'), [x.encode('UTF8') for x in result['description']['tags']]
			

	def processRequest( self, json, data, headers, params = None ):

		"""
		Helper function to process the request to Project Oxford

		Parameters:
		json: Used when processing images from its URL. See API Documentation
		data: Used when processing image read from disk. See API Documentation
		headers: Used to pass the key information and the data type request
		"""

		retries = 0
		result = None

		while True:
				response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
				if response.status_code == 429: 
						print "Message: %s" % ( response.json()['error']['message'] )
						if retries <= _maxNumRetries: 
								time.sleep(1) 
								retries += 1
								continue
						else: 
								print 'Error: failed after retrying!'
								break
				elif response.status_code == 200 or response.status_code == 201:
						if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
								result = None 
						elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
								if 'application/json' in response.headers['content-type'].lower(): 
										result = response.json() if response.content else None 
								elif 'image' in response.headers['content-type'].lower(): 
										result = response.content
				else:
						print "Error code: %d" % ( response.status_code )
						print "Message: %s" % ( response.json()['error']['message'] )
				break
		return result

	def get_image_description(self):
		if self.urlImage.find('http') != -1:
			description, tags = self.get_clould_image_description()
			return description, tags
		else:
			description, tags = self.get_local_image_description()
			return description, tags 