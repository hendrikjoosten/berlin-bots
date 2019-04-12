"""Computer Vision API snippets 
Based on https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/5e0cdeda77a84fcd9a6d3d0a
Functions:
    describe_image: returns one or more description of image
    detect_objects: returns objects found and bounding boxes
    analyze_image:  returns category, tags and one description 
See Usage at the bottom
"""


import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import os

#NOTE: For Testing on PC or PI
if True: 
    # URL
    contentType = 'application/json'
    body = "{'url':'image link here'}"
# For RaspberryPI ( set the if to False and specify a correct path in the Pi to save the image)
# it will take a temporary picture and send as binary file
else:
    # Takes picture on the pi as me.png
    os.system('raspistill -o {}'.format("/home/pi/Robuzure/me.png"))
    print('Photo was Taken')
    contentType = 'application/octet-stream'
    # CHANGE PATH TO PI
    body = open('/home/pi/Robuzure/me.png', 'rb')


# content type configured for images as binary files
headers = {
    # Request headers
    'Content-Type': contentType,
    'Ocp-Apim-Subscription-Key': 'a83b038ae8c14c85929d5bba098933c8'
}


def describe_image(img, number_of_descriptions=1):
    '''Returns a number_of_descriptions from an image'''
    params = urllib.parse.urlencode({
    # Request parameters
    'maxCandidates': "{}".format(number_of_descriptions),
    'language': 'en'})

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        # img recieves the binary image (body)
        conn.request("POST", "/vision/v2.0/describe?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())
        
        for i in range(len(r['description']['captions'])):
            print(r['description']['captions'][i]['text'])

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def detect_objects(img):
    ''''''
    global found_objects
    found_objects = []
    params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())
        print(data)
        print(r.keys())
        print("In the image of size {} by {} pixels, {} objects were detected".format(r['metadata']['width'], r['metadata']['height'], 
                                                                                      len(r['objects']))) 
        for i in r['objects']:
            # acessing the rectangle key
            found_objects.append(i['object'])
            print('{} detected at region {}'.format(i['object'], i['rectangle']))
        # print(found_objects) can be read by speaker
        # DRAW BOUNDING BOXES into Image with CV2?
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def analyze_image(img, visualFeatures='Description, Categories, Faces'):
    '''visualFeatures: a string of comma separated keywords 'Brands, Adult, Objects'
       Category of Image
       Tags of the image'''
    global speak
    params = urllib.parse.urlencode({
        # Request parameters
        'visualFeatures': '{}'.format(visualFeatures),
        'details': '',
        'language': 'en',
    })

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/analyze?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())

        # Handling Response in some useful manner. JSON has a lot of keys.
        # if r['faces'] == []:
        #    print('No faces encountered')
        
        # extracting tags
        print("Tags found in the image {}".format(r['description']['tags']))
        # send to some text generator service

        if "Description" in visualFeatures:
            speak = (r['description']['captions'][0]['text'])

        print(speak)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))




#NOTE: USAGE with example image: https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg
#      Uncomment the functions to test it!

#describe_image(body, number_of_descriptions=3)
    #>>a crowded city street filled with traffic at night
    #>>a group of people on a city street filled with traffic at night
    #>>a close up of a busy city street filled with traffic at night


#detect_objects(body)
    #>> In the image of size 1826 by 2436 pixels, 5 objects were detected
    #>> taxi detected at region {'x': 1277, 'y': 2057, 'w': 363, 'h': 231}
    #>> person detected at region {'x': 0, 'y': 2222, 'w': 174, 'h': 213}
    #>> person detected at region {'x': 199, 'y': 2224, 'w': 299, 'h': 206}
    #>> person detected at region {'x': 434, 'y': 2176, 'w': 236, 'h': 251}
    #>> person detected at region {'x': 826, 'y': 2161, 'w': 255, 'h': 270}
    #>> ['taxi', 'person', 'person', 'person']
# In PI one could: to tell the objects it finds
    # os.system('bash speak.sh "{}"'.format(found_objects)


analyze_image(body)
    #>>No faces encountered
    #>>Category of image: outdoor_street
    #>>Tags found in the image ['outdoor', 'building', 'street', 'city', 'busy', 'traffic', 'filled', 'people', 'car', 'walking', 'many', 'crowded', 'bunch', 'group', 'night', 'large', 'table', 'light', 'man', 'standing', 'umbrella', 'riding', 'tall', 'sign', 'rain', 'road']
    #>>a crowded city street filled with traffic at night
# In PI one could: to speak what it sees
    #os.system('bash speak.sh "{}"'.format(speak))

