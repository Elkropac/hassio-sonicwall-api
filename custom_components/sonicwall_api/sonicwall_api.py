from io import BytesIO
import logging
import simplejson as json
import pycurl

class SonicWallApi:
    """Class for SonicwallAPI"""

    _headers = ("Content-Type: application/json", "Accept: application/json")

    def __init__(self, base_url, username, password, verify_cert=False, login_override=False, login_method='basic'):
        """Initialize object"""
        self._base_url = base_url
        self._username = username
        self._password = password
        self._login_override = login_override
        self._login_method = login_method


        self._curl = pycurl.Curl()
        self._curl.setopt(pycurl.USERAGENT, "pycurl/HA/sonicwall_api")
        self._curl.setopt(pycurl.SSL_VERIFYPEER, verify_cert)
        self._curl.setopt(pycurl.SSL_VERIFYHOST, verify_cert)
        self._curl.setopt(pycurl.FORBID_REUSE, False)
        self._curl.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_1)
        self._curl.setopt(pycurl.CONNECTTIMEOUT, 5)
        self._curl.setopt(pycurl.VERBOSE, 0)

    def login(self):
        post = {'override': self._login_override}

        if self._login_method == 'chap':
            response = self.get('/auth')
            post['id'] = response['id']
            post['user'] = self._username
            #post['digest'] = md5(hex2bin($req->id).$this->pass.hex2bin($req->challenge))
        elif self._login_method == 'digest' or self._login_method == 'basic':
            self._curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST if (self._login_method == 'digest') else pycurl.HTTPAUTH_BASIC)
            self._curl.setopt(pycurl.USERNAME, self._username)
            self._curl.setopt(pycurl.PASSWORD, self._password)
        else:
            print("Unknown login method\n")
            exit(1)

        return self.post('/auth', post)

    def logout(self):
        return self.delete('/auth')

    def commit_changes(self):
        return self.post('/config/pending')

    def get(self, url):
        return self.get_delete(url, 'GET')

    def delete(self, url):
        return self.get_delete(url, 'DELETE')

    def post(self, url, data={}):
        return self.post_put_patch(url, data, 'POST')

    def put(self, url, data={}):
        return self.post_put_patch(url, data, 'PUT')

    def patch(self, url, data={}):
        return self.post_put_patch(url, data, 'PATCH')

    def get_delete(self, url, http_method='GET'):
        data = BytesIO()

        self._curl.setopt(pycurl.WRITEFUNCTION, data.write)
        self._curl.setopt(pycurl.CUSTOMREQUEST, http_method)
        self._curl.setopt(pycurl.POSTFIELDS, '')
        self._curl.setopt(pycurl.HTTPHEADER, self._headers)
        self._curl.setopt(pycurl.URL, self._base_url + url)
        response = self._curl.perform()

        return json.loads(data.getvalue())

    def post_put_patch(self, url, sendData={}, http_method='POST'):
        data = BytesIO()
        self._curl.setopt(pycurl.WRITEFUNCTION, data.write)
        self._curl.setopt(pycurl.CUSTOMREQUEST, http_method)

        headers = list(self._headers)
        if len(sendData) > 0:
            send = json.dumps(sendData)+"\r\n"
            self._curl.setopt(pycurl.POSTFIELDS, send)
            headers.append("Content-Length: %d" % len(send))
        else:
            self._curl.setopt(pycurl.POSTFIELDS, '')
            headers.append("Content-Length: 0")

        self._curl.setopt(pycurl.HTTPHEADER, headers)
        self._curl.setopt(pycurl.URL, self._base_url + url)

        response = self._curl.perform()

        return json.loads(data.getvalue())
