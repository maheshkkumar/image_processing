import time 
import requests
import cv2
import operator
import numpy as np
import sys

# Variables

_url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = 'bfe4672a06364a60899ed0faab481e15'
_maxNumRetries = 10

def processRequest( json, data, headers, params = None ):

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
                    print result
        else:
            print "Error code: %d" % ( response.status_code )
            print "Message: %s" % ( response.json()['error']['message'] )
        break
    return result

# def renderResultOnImage( , result, img ):

   #  """Display the obtained results onto the input image"""

   #  for currFace in result:
   #      faceRectangle = currFace['faceRectangle']
   #      cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
   #                         (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
   #                     color = (255,0,0), thickness = 1 )
   #      faceLandmarks = currFace['faceLandmarks']
   #      for _, currLandmark in faceLandmarks.iteritems():
   #          cv2.circle( img, (int(currLandmark['x']),int(currLandmark['y'])), color = (0,255,0), thickness= -1, radius = 1 )
   #  for currFace in result:
   #      faceRectangle = currFace['faceRectangle']
   #      faceAttributes = currFace['faceAttributes']
   #      textToWrite = "%c (%d)" % ( 'M' if faceAttributes['gender']=='male' else 'F', faceAttributes['age'] )
   #      cv2.putText( img, textToWrite, (faceRectangle['left'],faceRectangle['top']-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1 )


def detect_cloud_image():
	
	# Face detection parameters
	params = { 'returnFaceAttributes': 'age,gender', 
	           'returnFaceLandmarks': 'true'} 
	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/json' 
	json = { 'url': urlImage }
	data = None
	result = processRequest( json, data, headers, params )
	return result

def detect_local_image(urlImage):

	complete_url = '/home/mahesh/visual_lifelog/image_processing/'+urlImage 
	print complete_url
	with open( complete_url, 'rb' ) as f:
	    data = f.read()
	# Face detection parameters
	params = { 'returnFaceAttributes': 'age,gender', 
	           'returnFaceLandmarks': 'true'} 
	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'
	json = None
	result = processRequest( json, data, headers, params )
	print result

if __name__ == '__main__':
	detect_local_image(sys.argv[1])