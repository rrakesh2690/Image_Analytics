import httplib, urllib, base64, json

# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'de8b6e5c6d1f4dee8fc433e5ab4bb713'

uri_base = 'westeurope.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})

# The URL of a JPEG image to analyze.
read_img = r'C:\Users\acrotrend9\Desktop\pics\food_pic.jpg'
with open( read_img, 'rb' ) as f:
    body = f.read()
    
#body = "{'url':'https://en.wikipedia.org/wiki/File:President_Barack_Obama.jpg'}"

try:
    # Execute the REST API call and get the response.
    conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)