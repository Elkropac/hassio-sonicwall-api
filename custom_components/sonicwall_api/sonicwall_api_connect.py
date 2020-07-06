from .const import (
    LOGGER
)

from .errors import AlreadyConfigured, AuthenticationRequired, CannotConnect

import hashlib
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib3.exceptions import InsecureRequestWarning

#debug
#import http.client as http_client
#http_client.HTTPConnection.debuglevel = 1

class SonicWallApi_Connect:
    """Class for SonicwallAPI_Connect"""

    _headers = {"Content-Type": "application/json", "Accept": "application/json", "Accept-Encoding": "application/json", "User-Agent": "requests/HA/sonicwall_api"}
    _timeout = 5

    def __init__(self, base_url, username, password, verify_ssl=False, login_override=False, login_method='basic'):
        """Initialize object"""
        self._base_url = base_url
        self._verify = verify_ssl
        self._username = username
        self._password = password
        self._login_override = login_override
        self._login_method = login_method
        if self._verify == False:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def login(self):
        post = {'override': self._login_override}

        if self._login_method == 'chap':
            self._auth = ''
            response = self.get('/auth', True)
            post['id'] = response.json()['id']
            post['user'] = self._username
            post['digest'] = hashlib.md5(bresponse.json()['id'].decode('hex')+self._password+response.json()['challenge'].decode('hex'))
        elif self._login_method == 'basic':
            self._auth = HTTPBasicAuth(self._username, self._password)
        elif self._login_method == 'digest':
            self._auth = HTTPDigestAuth(self._username, self._password)
        else:
            print("Unknown login method\n")
            exit(1)

        return self.post('/auth', post)

    def logout(self):
        return self.delete('/auth')

    def commit_changes(self):
        return self.post('/config/pending')

    def get(self, url, ignore_401 = False):
        r = requests.get(self._base_url + url, auth=self._auth, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        if r.status_code == 401 and ignore_401 == True:
          return r
        r.raise_for_status()
        return r

    def delete(self, url):
        r = requests.delete(self._base_url + url, auth=self._auth, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        return r

    def post(self, url, data={}):
        r = requests.post(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        r.raise_for_status()
        return r

    def put(self, url, data={}):
        r = requests.put(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        r.raise_for_status()
        return r

    def patch(self, url, data={}):
        r = requests.patch(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        r.raise_for_status()
        return r

"""
        try:
            r = requests.get(self._base_url + url, auth=self._auth, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as err:
            #print ("OOps: Something Else",err)
            raise CannotConnect
        except requests.exceptions.HTTPError as errh:
            #print ("Http Error:",errh)
            raise CannotConnect
        except requests.exceptions.ConnectionError as errc:
            #print ("Error Connecting:",errc)
            raise CannotConnect
        except requests.exceptions.Timeout as errt:
           #print ("Timeout Error:",errt)
            raise CannotConnect
"""