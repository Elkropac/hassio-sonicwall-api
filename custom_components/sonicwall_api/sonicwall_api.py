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

class SonicWallApi:
    """Class for SonicwallAPI"""

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
            response = self.get('/auth')
            post['id'] = response.json['id']
            post['user'] = self._username
            post['digest'] = hashlib.md5(bresponse.json['id'].decode('hex')+self._passowrd+response.json['challenge'].decode('hex'))
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

    def get(self, url):
        r = requests.get(self._base_url + url, auth=self._auth, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        r.raise_for_status()
        return r
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

    def delete(self, url):
        r = requests.delete(self._base_url + url, auth=self._auth, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        return r

    def post(self, url, data={}):
        r = requests.post(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        r.raise_for_status()
        return r
        try:
            r = requests.post(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
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

    def put(self, url, data={}):
        r = requests.put(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        return r

    def patch(self, url, data={}):
        r = requests.patch(self._base_url + url, auth=self._auth, json=data, verify=self._verify, headers=self._headers, stream=False, timeout=self._timeout)
        return r

async def get_api(
    hass, url, username_rw, password_rw, verify_ssl, login_override, login_method
):

    url = url + '/api/sonicos'

    api = SonicWallApi(
        url,
        username=username_rw,
        password=password_rw,
        verify_ssl=verify_ssl,
        login_override=login_override,
        login_method=login_method
    )

    try:
        login = api.login()
        if (login.status_code == 401):
          LOGGER.warning("Connected to UniFi at %s but not registered.", host)
          raise AuthenticationRequired
        return api
    except requests.exceptions.RequestException:
        LOGGER.error("Error connecting to the UniFi controller at %s", host)
        raise CannotConnect
#    except aiounifi.Unauthorized:
#        LOGGER.warning("Connected to UniFi at %s but not registered.", host)
#        raise AuthenticationRequired

#    except (asyncio.TimeoutError, aiounifi.RequestError):
#        LOGGER.error("Error connecting to the UniFi controller at %s", host)
#        raise CannotConnect

#    except aiounifi.AiounifiException:
#        LOGGER.exception("Unknown UniFi communication error occurred")
#        raise AuthenticationRequired
