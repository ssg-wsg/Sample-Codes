from requests_oauthlib import OAuth2Session

print('################################################################\n'
      'Simple Program in Python to call OAuth 2 Token for Get API\n'
      '################################################################\n'
      '1) Please get ready the GET API URL\n'
      '2) Please get ready the Client ID from developer portal\n'
      '3) Please get ready the Secret from developer portal\n')


try:
    "request for url, client_id and client secret"
    request_url = input("Enter URL to continue: ")
    client_id = input("Enter Client Id: ")
    client_secret = input("Input Secret Key: ")

    "function to fetch the token from the url inserted"
    from oauthlib.oauth2 import BackendApplicationClient

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url='https://public-api.ssg-wsg.sg/dp-oauth/oauth/token',
        client_id=client_id,
        client_secret=client_secret
    )

    response = oauth.get(request_url)
    print("Status Code= ", response.status_code)
    print(response.json())
    
except:
    print("An error has occurred. Please check data input")