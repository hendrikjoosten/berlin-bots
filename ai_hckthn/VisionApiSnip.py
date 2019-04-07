
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

# Select URL or LOCAL FILE
if False:
    # URL
    contentType = 'application/json'
    body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
else:
    # LOCAL FILE
    contentType = 'application/octet-stream'
    body = open('wacky.jpeg', 'rb')


headers = {
    # Request headers
    'Content-Type': contentType,
    'Ocp-Apim-Subscription-Key': '288a5ff36384430da7dd849957c8540e',
}

params = urllib.parse.urlencode({
})


try:
    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v2.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
