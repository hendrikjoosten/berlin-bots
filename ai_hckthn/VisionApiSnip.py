
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

# Select URL or LOCAL FILE
if False:
    # URL
    contentType = 'application/json'
    body = "{'url':'image link heres'}"
else:
    # LOCAL FILE
    contentType = 'application/octet-stream'
    body = open('wacky.jpg', 'rb')


headers = {
    # Request headers
    'Content-Type': contentType,
    'Ocp-Apim-Subscription-Key': 'a83b038ae8c14c85929d5bba098933c8',
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
