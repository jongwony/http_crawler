import os
import time

from virtualenv import PathEnv
from src.log import Log
PathEnv.apply_virtualenv('.py3')
import requests


class Crawl:
    def __init__(self, log_path):
        self.session = requests.Session()
        self.log = Log(log_path)

    def make_response(self, requests_parameter, sleep):
        """
        Crawling page or data using 'requests' module

        :param requests_parameter: {
            method = 'GET',
            url = base_url + path,
            params = dictionary or inline string,
            headers = dictionary,
        }
        :param sleep: time.sleep
        :return: requests.response
        """
        response = self.session.request(**requests_parameter, timeout=10)
        if response.headers.get('status'):
            if '200' not in response.headers['status']:
                self.log.warning('HTTP Status Error!, {}'.format(str(response.headers)))

        time.sleep(sleep)
        return response

    def __del__(self):
        print('session_closed!')
        self.session.close()
