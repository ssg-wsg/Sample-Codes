import requests

print('################################################################\n'
      'Simple Program in Python to use certificate generated for Get API\n'
      '################################################################\n'
      'Please get ready the GET API URL\n')

try:
        request_url = input("Enter URL to continue: ")
        response = requests.get(request_url, cert=('/Users/Ming/SampleCode/cert.pem', '/Users/Ming/SampleCode/key.pem')
                                )
        print("Status Code: ", response.status_code)
        print(response.json())
except:
        print("Please check whether input URL or certificate path is valid")
