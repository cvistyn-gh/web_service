# import requests
# import os
# from io import BytesIO
# import base64

# r = requests.get('http://localhost:5000/')
# print(r.status_code)
# print(r.text)
# r = requests.get('http://localhost:5000/data_to')
# print(r.status_code)
# print(r.text) 
# r = requests.get('http://localhost:5000/net')
# print(r.status_code)
# print(r.text) 

# img_data = None
# path = os.path.join('./static','image0008.png')
# with open(path, 'rb') as fh:
    # img_data = fh.read()
    # b64 = base64.b64encode(img_data)
# jsondata = {'imagebin':b64.decode('utf-8')}
# res = requests.post('http://localhost:5000/apinet', json=jsondata)
# if res.ok:
    # print(res.json())

# try:
    # r = requests.get('http://localhost:5000/apixml')
    # print(r.status_code)
    # if(r.status_code!=200):
        # exit(1)
    # print(r.text)
# cept:
    # exit(1)

import requests
import os
from io import BytesIO
import base64

RENDER_URL = "https://web-service-lab1.onrender.com"

print(f"Testing application at: {RENDER_URL}")


try:
    r = requests.get(f'{RENDER_URL}/')
    print(f"Main page status: {r.status_code}")
    if r.status_code == 200:
        print("✓ Main page is working")
    else:
        print(f"✗ Main page error: {r.text}")
except Exception as e:
    print(f"✗ Main page request failed: {e}")

try:
    r = requests.get(f'{RENDER_URL}/data_to')
    print(f"Data page status: {r.status_code}")
    if r.status_code == 200:
        print("✓ Data page is working")
    else:
        print(f"✗ Data page error: {r.text}")
except Exception as e:
    print(f"✗ Data page request failed: {e}")

try:
    r = requests.get(f'{RENDER_URL}/net')
    print(f"Net page status: {r.status_code}")
    if r.status_code == 200:
        print("✓ Net page is working")
    else:
        print(f"✗ Net page error: {r.text}")
except Exception as e:
    print(f"✗ Net page request failed: {e}")

try:
    img_data = None
    path = os.path.join('./static','image0008.png')

    if os.path.exists(path):
        with open(path, 'rb') as fh:
            img_data = fh.read()
            b64 = base64.b64encode(img_data)

        jsondata = {'imagebin': b64.decode('utf-8')}
        print("Sending image to API...")

        res = requests.post(f'{RENDER_URL}/apinet', json=jsondata, timeout=30)
        if res.ok:
            print("✓ API Response successful:")
            print(res.json())
        else:
            print(f"✗ API Error: {res.status_code} - {res.text}")
    else:
        print(f"✗ Test image not found at: {path}")

except Exception as e:
    print(f"✗ API request failed: {e}")


try:
    r = requests.get(f'{RENDER_URL}/apixml', timeout=10)
    print(f"XML API status: {r.status_code}")
    if r.status_code == 200:
        print("✓ XML API is working")
        # print(r.text)
    else:
        print(f"✗ XML API error: {r.status_code}")
        exit(1)
except Exception as e:
    print(f"✗ XML API request failed: {e}")
    exit(1)

print("\n" + "="*50)
print("Testing completed!")
