import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bfe4672a06364a60899ed0faab481e15',
}

params = urllib.urlencode({
    "faceId1":"c5c24a82-6845-4031-9d5d-978df9175426",
    "faceId2":"015839fb-fbd9-4f79-ace9-7675fc2f1dd9" 
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v1.0/verify?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
