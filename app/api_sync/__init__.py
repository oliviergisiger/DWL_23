from abc import ABC, abstractmethod
import requests



class APIToken(ABC):

    @abstractmethod
    def update_token(self):
        pass


class SRGToken(APIToken):

    def __init__(self):
        self.oauth_token = self.update_token()

    def update_token(self):
        headers = {
            'Authorization': 'Basic aUtRQk9YdkFvdFY4S3oxOXBxZWVOQWM1WkkwZTlNdTk6OENMck9ZOUk5ZHVBWGRrTQ==',
            'Content-Length': '0'
        }
        url = 'https://api.srgssr.ch/oauth/v1/accesstoken?grant_type=client_credentials'
        response = requests.post(url=url, headers=headers).json()
        return response['access_token']


