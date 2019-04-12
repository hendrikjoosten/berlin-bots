# Initializer 
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import os, requests
import numpy as np
import time

# Initializer
# Subscriptions
subscriptions_dict = {'computer_vision':'c0fd5de0a7eb4ad9a241d1fe1f4cd989',
                      'face_api': 'cd91c79a18534dc58d7eae4608ea3d3d',
                      'speech_api': 'd3015735e75546cd9af885976b8e4c54',
                      'text_analytics': 'bcf64cde5aad4e09856471aa6530026f',
                      'luis':'2a2b546798854097ace2140bf961a493',
                      'translation':'f9f3e098ebee47158a222aeef0cf8db7'}

# Request Headers
headers = {'Content-Type': 'applications/json',
            'Ocp-Apim-Subscription-Key': subscriptions_dict['computer_vision']}

# Content body to be sent, many forms, to be redefined
body = "{'url':'https://pbs.twimg.com/profile_images/1062098998746644480/JTIpfWME_400x400.jpg'}"
# _ _ _ _  _ _ 
# The target body for is changed using these two functions
def change_headers(contentType='application/json', api='computer_vision'):
    '''At the beginning of every function to ensure proper settings'''
    global headers
    headers = {'Content-Type': contentType,
               'Ocp-Apim-Subscription-Key':subscriptions_dict[api]}

# Camera for Pi 
# Takes picture by calling the raspistill command in the terminal and defines it as body
def body_take_picture(name='me', pic=True):
    """defines body as binary image data of the picture taken, 
       required for comptuer vision api
       global body, headers"""
    global body, headers
    headers['Content-Type'] = 'application/octet-stream'
    if pic==True:
        os.system('raspistill -o {}'.format("/home/pi/Robuzure/{}.png".format(name)))
        print('Picture taken')
    body = open('/home/pi/Robuzure/{}.png'.format(name), 'rb')


# For Test in PC
def body_url_image(url='https://pbs.twimg.com/profile_images/1062098998746644480/JTIpfWME_400x400.jpg'):
    global headers, body
    headers['Content-Type'] = 'application/json'
    body = "{'url':'%s'}"%url
    return body
    
#NOTE: COMPUTER VISION _ _ _ _ _ _ _

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
    '''global found_objects'''
    global found_objects
    found_objects = []
    params = urllib.parse.urlencode({})
    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        
        # print(found_objects) can be read by speaker
        # DRAW BOUNDING BOXES into Image with CV2?
        conn.request("POST", "/vision/v2.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())
        #print(data)
        print(r.keys())
        print("In the image of size {} by {} pixels, {} objects were detected".format(r['metadata']['width'], r['metadata']['height'], 
                                                                                      len(r['objects']))) 
        print(len(r['objects']))                                                                           
        if len(r['objects']) == '0':
            print('this happened')
            return None
        else:
            for i in r['objects']:
                # acessing the rectangle key
                found_objects.append(i['object'])
                print('{} detected at region {}'.format(i['object'], i['rectangle']))
        # print(found_objects) can be read by speakerfor
        # DRAW BOUNDING BOXES into Image with CV2?
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def analyze_image(img, visualFeatures='Description, Categories, Faces'):
    '''Global speak variable `
       visualFeatures: a string of comma separated keywords 'Brands, Adult, Objects'
       Category of Image
       Tags of the image'''
    global speak
    params = urllib.parse.urlencode({
        # Request parameters
        'visualFeatures': '{}'.format(visualFeatures),
        'details': '',
        'language': 'en'})

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/analyze?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())

        # Handling Response in some useful manner. JSON has a lot of keys.
        #if r['faces'] == []:
         #   print('No faces encountered')
        #else:
        #    print('At least a face was detected')
        print("Category of image: {}".format(r['categories'][0]['name']))
        
        # extracting tags
        print("Tags found in the image {}".format(r['description']['tags']))
        # send to some text generator service

        
        speak = (r['description']['captions'][0]['text'])

        print(speak)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Set up with image
#body_url_image(url='https://pbs.twimg.com/profile_images/1062098998746644480/JTIpfWME_400x400.jpg')
# set up headers
#change_headers(contentType='application/json', api='computer_vision')
# Calling Functions
#describe_image(body, number_of_descriptions=3)
#analyze_image(body)
#print(body)
#detect_objects(body)

## THIS IS THE PROBLEM!

# FACE API
def detect_face(img):
    '''global `info`, describes age, gender and emotion'''
    global info, r
    
    """Find attributes of a human face age, gender, emotions etc."""
    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair',
        'recognitionModel': 'recognition_01',
        'returnRecognitionModel': 'false',
    })

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        #print(data)
        r = json.loads(data.decode())
    
        print('{} face(s) were found'.format(len(r)))

        for face_info in r:
            attributes = face_info['faceAttributes']
            #print("Face Info ", attributes, '\n')
            highest_emotion_index = np.argmax(list(attributes['emotion'].values()))
            #print(highest_emotion_index)
            info = "A {} of around {} years with a {} of {} percent".format(attributes['gender'], 
                                                                            attributes['age'], 
                                                                            list(attributes['emotion'].keys())[highest_emotion_index],
                                                                           int(max(attributes['emotion'].values())*100))
            print(info)
            
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# EXAMPLES:

# Take a picture of yourself. Get back gender, age and emotion as audio (info variable)
#body_take_picture()
#change_headers(contentType='application/octet-stream', api='face_api')
#detect_face(body)
#print(info)
#os.system('bash speak.sh "{}"'.format(info))


# Speak what it sees in an URL image
#body_url_image(url='https://pbs.twimg.com/profile_images/1062098998746644480/JTIpfWME_400x400.jpg')
# set up headers
#change_headers(contentType='application/json', api='computer_vision')
# function using body
#detect_objects(body)
#os.system('bash speak.sh "{}"'.format(found_objects))


# Speak what it sees with the camera
#body_take_picture()
#change_headers(contentType='application/octet-stream', api='computer_vision')
#analyze_image(body)
#print('To be spoken ', speak)
#os.system('bash speak.sh "{}"'.format(speak))




# Text Analytics API

TextToAnalyze = 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.\nNow we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battlefield of that war.\nWe have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.\nBut, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract.\nThe world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced.\nIt is rather for us to be here dedicated to the great task remaining before us that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion, that we here highly resolve that these dead shall not have died in vain; that this nation, under God, shall have a new birth of freedom and that government of the people, by the people, for the people, shall not perish from the earth.'
def text_body(TextToAnalyze=TextToAnalyze):
    """To create a body of a single text to be analyzed. The (same Id to track more documents)"""
    global body
    body = {
        # to this list you can add more dictionaries {lang, id, text..} to analyze more than one text
      "documents": [
        {
            "id": "TextTest",
            "text": "'{}'".format(TextToAnalyze)
        }]}


def detect_language(text):
    '''Only for one '''
    global detected_language
    textAnalyticsURI = 'westeurope.api.cognitive.microsoft.com'
    params = urllib.parse.urlencode({})
    text_body(text)
    try:
        conn = http.client.HTTPSConnection(textAnalyticsURI)
        conn.request("POST", "/text/analytics/v2.0/languages?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        r = json.loads(data.decode())
        detected_language = r['documents'][0]['detectedLanguages'][0]['name']
        print(detected_language)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))





def key_phrases(text):
    # Define the parameters
    textAnalyticsURI = 'westeurope.api.cognitive.microsoft.com'
    params = urllib.parse.urlencode({})
    text_body(text)
    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection(textAnalyticsURI)
        conn.request("POST", "/text/analytics/v2.0/keyPhrases?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # 'data' contains the JSON response, which includes a collection of documents.
        parsed = json.loads(data)
        for document in parsed['documents']:
            print("Document " + document["id"] + " key phrases:")
            for phrase in document['keyPhrases']:
                print("  " + phrase)
            print("---------------------------")
        conn.close()

    except Exception as e:
        print('Error:')
        print(e)

#change_headers(contentType='application/json',api='text_analytics')
#dracula_letter = '''My good Friend, When I received your letter I am already coming to you. By good fortune I can leave just at once, without wrong to any of those who have trusted me. Were fortune other, then it were bad for those who have trusted, for I come to my friend when he call me to aid those he holds dear. Tell your friend that when that time you suck from my wound so swiftly the poison of the gangrene from that knife that our other friend, too nervous, let slip, you did more for him when he wants my aids and you call for them than all his great fortune could do. But it is pleasure added to do for him, your friend, it is to you that I come. Have near at hand, and please it so arrange that we may see the young lady not too late on tomorrow, for it is likely that I may have to return here that night. But if need be I shall come again in three days, and stay longer if it must. Till then goodbye, my friend John.'''
#key_phrases(dracula_letter)

def check_sentiment(text):
     # Define the parameters
    textAnalyticsURI = 'westeurope.api.cognitive.microsoft.com'
    change_headers(api='text_analytics')
    params = urllib.parse.urlencode({})
    text_body(text)
    try:
        conn = http.client.HTTPSConnection(textAnalyticsURI)
        conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        parsed = json.loads(data) 
        # Get the numeric score for each document
        for document in parsed['documents']:
            sentiment = "negative"
            # if it's more than 0.5, consider the sentiment to be positive.
            if document["score"] >= 0.5:
                sentiment = "positive"
            print("Document:" + document["id"] + " = " + sentiment)
        conn.close()
    
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#change_headers(contentType='application/json',api='text_analytics')
#dracula_letter = '''My good Friend, When I received your letter I am already coming to you. By good fortune I can leave just at once, without wrong to any of those who have trusted me. Were fortune other, then it were bad for those who have trusted, for I come to my friend when he call me to aid those he holds dear. Tell your friend that when that time you suck from my wound so swiftly the poison of the gangrene from that knife that our other friend, too nervous, let slip, you did more for him when he wants my aids and you call for them than all his great fortune could do. But it is pleasure added to do for him, your friend, it is to you that I come. Have near at hand, and please it so arrange that we may see the young lady not too late on tomorrow, for it is likely that I may have to return here that night. But if need be I shall come again in three days, and stay longer if it must. Till then goodbye, my friend John.'''
#check_sentiment(dracula_letter)

# still unparsed results, but perhaps helpful later
def find_entities(text):
    params = urllib.parse.urlencode({})
    text_body(text)
    textAnalyticsURI = 'westeurope.api.cognitive.microsoft.com'
    change_headers(api='text_analytics')
    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/entities?%s" % params, str(body), headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#change_headers(contentType='application/json',api='text_analytics')
#dracula_letter = '''My good Friend, When I received your letter I am already coming to you. By good fortune I can leave just at once, without wrong to any of those who have trusted me. Were fortune other, then it were bad for those who have trusted, for I come to my friend when he call me to aid those he holds dear. Tell your friend that when that time you suck from my wound so swiftly the poison of the gangrene from that knife that our other friend, too nervous, let slip, you did more for him when he wants my aids and you call for them than all his great fortune could do. But it is pleasure added to do for him, your friend, it is to you that I come. Have near at hand, and please it so arrange that we may see the young lady not too late on tomorrow, for it is likely that I may have to return here that night. But if need be I shall come again in three days, and stay longer if it must. Till then goodbye, my friend John.'''
#find_entities(dracula_letter)


# SPEECH API _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
#NOTE: MUST RUN THIS to Get Token for 10 minutes: This needs to be handled more smartly (keeping track of time for example...)
change_headers(contentType='application/json', api='speech_api')
response = requests.post('https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken', headers=headers)
accesstoken = str(response.text)

def speech_to_text(path_to_wav, language='en-US'):
    '''Input a wav file, returns text
    lang: en-US, de-DE, es-MX, ru-RU, pt-PT'''
    global speech_result
    with open("{}".format(path_to_wav), mode="rb") as audio_file:
        audio_data =  audio_file.read()
    type(audio_data)
    # Now that we have a token, we can set up the request
    speechToTextEndPoint = "https://westeurope.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
    headers = {"Content-type": "audio/wav; codec=audio/pcm; samplerate=16000", 
            "Authorization": "Bearer " + accesstoken}
    params = {"language":language}
    body = audio_data

    # Connect to server, post the request, and get the result
    response = requests.post(speechToTextEndPoint,data=body, params=params, headers=headers)
    result = str(response.text)
    speech_result = json.loads(result)['DisplayText']
    print(speech_result)

#change_headers(contentType='application/json', api='speech_api')
#speech_to_text('/home/pi/Robuzure/RainSpain.wav')

# Function to record wav file from the pi
def record(seconds):
    print('Recording for {} seconds'.format(seconds))
    # arecord + flags for better quality than default (unusable)
    os.system('arecord -f S16_LE -c2 -r 44100 -d {} temp.wav'.format(seconds))

#SHOULD WORK, but Microphone it's not the best. WORKING
#record(seconds=5)
#speech_to_text('/home/pi/Robuzure/temp.wav')


### LUIS => Made a simple app with two intents: Take Picture or Record Audio
# It requires to have the app id and the subscription id in the ENDPOINT.

def get_intent(text):
    import requests
    global intent
    params ={
        # Query parameter
        'q': ''.format(text),
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
        'subscription-key':'1b91b846370b41e8b9277ab927fb558c'}

    try:
        #r = requests.get('https://westeurope.api.cognitive.microsoft.com/luis/v2.0/apps/df46b650-b9f9-4489-b9f8-74532e9fd247',headers=headers, params=params)
        r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/df46b650-b9f9-4489-b9f8-74532e9fd247?verbose=true&timezoneOffset=-360&subscription-key=1b91b846370b41e8b9277ab927fb558c&q={}'.format(text))
        r = json.loads((r.content).decode())
        print(r['topScoringIntent'])
        intent = r['topScoringIntent']['intent']

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

# WORKS!: We can record(audio) => speech_to_text(audio.wav) => LUIS Model => Intent => control the pi by voice commands

#change_headers(contentType='application/json', api='luis')
#get_intent('Take a picture with the camera')
#os.system('bash speak.sh "{}"'.format(intent))


## Text Translate API

def translate_text(textToTranslate="Let's see if it works", fromLangCode='en', toLangCode='de'):
    import requests, http.client, urllib.request, urllib.parse, urllib.error, base64, json, urllib
    from xml.etree import ElementTree
    global translated_result
    try:
        # Connect to server to get the Access Token
        params = ""
        headers = {"Ocp-Apim-Subscription-Key": subscriptions_dict['translation']}
        AccessTokenHost = "api.cognitive.microsoft.com"
        path = "/sts/v1.0/issueToken"

        conn = http.client.HTTPSConnection(AccessTokenHost)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        accesstoken = "Bearer " + data.decode("UTF-8")

        # Define the request headers.
        headers = {
            'Authorization': accesstoken}

        # Define the parameters
        params = urllib.parse.urlencode({
            "text": textToTranslate,
            "to": toLangCode,
            "from": fromLangCode})

        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection("api.microsofttranslator.com")
        conn.request("GET", "/V2/Http.svc/Translate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        translation = ElementTree.fromstring(data.decode("utf-8"))
        translated_result = translation.text
        print(translated_result)
        conn.close()
        
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

#change_headers(contentType='application/json',api='translation')
#translate_text("This should work, let's hope it does")
#>>Dies sollte funktionieren, hoffen wir, dass dies der Fall ist
#translate_text('So this is working quite well actually, cool stuff')
#>>So funktioniert das ganz gut eigentlich coole Sachen
# not the best grammar but seems alright!!! 
# instant language to language translation could be cool


def pi_speak(text, language='en-US'):
    os.system('pico2wave -l {} -w lookwave.wav "{}" && aplay lookwave.wav'.format(language, text))

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ CHAINS _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
# ___ Instant Translation from a language to another one ___ 
def instant_translation(fromLangCode='en', toLangCode='de', seconds=5):# botton to control end or not end?
    # For whatever reason the APIs use 2 different language notations o,O. Complicates stuff
    # Now 4 languages supported, if we need more add the right keys.
        # https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#speech-to-text
        # https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support
    match_langs ={'en':'en-US',
                  'de':'de-DE',
                  'pt':'pt-PT',
                  'es':'es-ES'}
    from_matched_lang = match_langs[fromLangCode]
    to_matched_lang = match_langs[toLangCode]
    record(seconds=seconds)
    change_headers(contentType='application/json', api='speech_api')
    speech_to_text('/home/pi/Robuzure/temp.wav', language=from_matched_lang)
    change_headers(contentType='application/json',api='translation')
    translate_text(speech_result, fromLangCode=fromLangCode, toLangCode=toLangCode)
    pi_speak(translated_result, language=to_matched_lang)

# Working alright :D
#instant_translation(fromLangCode='es', toLangCode='de') 

def infer_intent(seconds=5):
    '''Record voice and assign it to an intent of the LUIS app '''
    record(seconds=seconds)
    change_headers(contentType='application/json', api='speech_api')
    speech_to_text('/home/pi/Robuzure/temp.wav', language='en-US')
    change_headers(contentType='application/json', api='luis')
    get_intent('{}'.format(speech_result)) 
    print(intent)
    return(intent)

# Working :D
#task = infer_intent(seconds=3)  
#if task == 'Take Picture': # MORE THAN ONE CAMERA!! => SET UP TWO RASPBERRY PIS!!!! [][] MultiCores processes talking, system cant use all systems at once but if can if there are three. 
# Simulation... 
#   print("I'll take a picture!")

#change_headers(contentType='application/json', api='luis')
#get_intent('what do you see. record my voice') # CAN'T HANDLE MORE THAN ONE INTENT SO EASILY..!

# TO USE SEVERAL CV FUNCTIONS we need to redefine body.
# It seems like the stream of bytes is consumed 
def observe():
    global body
    # if body is not redefined after each function, it remains stuck!
    body_take_picture()
    change_headers(contentType='application/octet-stream', api='computer_vision')
    #describe_image(body)
    detect_objects(body)
    body = open('/home/pi/Robuzure/me.png','rb')
    print(body)
    analyze_image(body)
    body = open('/home/pi/Robuzure/me.png','rb')
    describe_image(body)
