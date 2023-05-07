from airflow import settings
from airflow.models import Connection
import requests
import re
import json
from datetime import time





def get_aws_session_credentials(expiration_time):
    URL = 'https://labs.vocareum.com/util/vcput.php?a=getaws&type=1&stepid=1569028&version=0&v=0&vockey=rUvDz4fZExx3whMjpx7S%2Bg%3D%3D'
    PARAMS = {
        'authority': 'labs.vocareum.com',
        'accept': '*/*',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': f'userid=2428323; usingLTI=1; vocuserid=2428323; myfolder=5bdbb6c1e99eed3754a27e43cbd1721f; currentcourse=vc_2_0_11992abdorg265_304; currentassignment=1569027; logintoken=5d88c860688dda17ec6dbf86d4387fad; tokenExpire={expiration_time}; usertoken=5d88c860688dda17ec6dbf86d4387fad; t2fausers=5d88c860688dda17ec6dbf86d4387fad',
        'referer': 'https://labs.vocareum.com/main/main.php?m=clabide&mode=s&asnid=1569029&stepid=1569030&hideNavBar=1',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = requests.get(url=URL, headers=PARAMS).text

    aws_key = re.search(r'aws_access_key_id=(.*)', resp).group(1)
    aws_secret = re.search(r'aws_secret_access_key=(.*)', resp).group(1)
    aws_session = re.search(r'aws_session_token=(.*)', resp).group(1)

    return {
        "aws_access_key_id": aws_key,
        "aws_secret_access_key": aws_secret,
        "aws_session_token": aws_session
    }


def update_connection(connection_id: str, _extra):
    session = settings.Session()
    session.query(Connection).filter(Connection.conn_id == connection_id).update({'extra': json.dumps(_extra)})
    session.commit()


if __name__ == '__main__':
    pass
