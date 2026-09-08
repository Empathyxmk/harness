#    Python Siesta
#
#    Copyright (c) 2008 Rafael Xavier de Souza
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Siesta is a REST client for python
"""

__version__ = "0.5.2"
__author__ = "Sebastian Castillo <castillobuiles@gmail.com>"
__contributors__ = []

import re
import time
try:
    import urllib.parse as urllib_parse
    import urllib.request as urllib_request
    import http.client as http_client
    from urllib.parse import urlparse
except ImportError:
    import urllib as urllib_parse
    import urllib as urllib_request
    import httplib as http_client
    from urlparse import urlparse

import logging
import simplejson as json

USER_AGENT = "Python-siesta/%s" % __version__

logging.basicConfig(level=0)

def _urlsplit(url):
    # Compatibility for both Python 2 and 3
    try:
        # For Python 3
        from urllib.parse import urlsplit as urlsplit_func
    except ImportError:
        # For Python 2
        from urlparse import urlsplit as urlsplit_func
    return urlsplit_func(url)

class Resource(object):

    def __init__(self, uri, api):
        self.api = api
        self.uri = uri
        split_parts = _urlsplit(self.api.base_url + self.uri)
        self.scheme = split_parts.scheme
        self.host = split_parts.netloc
        self.url = split_parts.path
        self.id = None
        self.conn = None
        self.headers = {'User-Agent': USER_AGENT}
        self.attrs = {}
        self._errors = {}
        
    def __getattr__(self, name):
        if name in self.attrs:
            return self.attrs.get(name)
        key = self.uri + '/' + name
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api)
        return self.api.resources[key]

    def __call__(self, id=None):
        if id is None:
            return self
        self.id = str(id)
        key = self.uri + '/' + self.id
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api)
        return self.api.resources[key]

    def set_request_type(self, mime):
        if mime.lower() == 'json':
            mime = 'application/json'
        elif mime.lower() == 'xml':
            mime = 'application/xml'
        self.headers['Accept'] = mime

    def get(self, **kwargs):
        if self.id is None:
            url = self.url
        else:
            url = self.url + '/' + str(self.id)
        if len(kwargs) > 0:
            try:
                query = urllib_parse.urlencode(kwargs)
            except AttributeError:
                # Python 2: urlib.urlencode
                query = urllib_parse.urlencode(kwargs)
            url = "%s?%s" % (url, query)
        self._request("GET", url)
        return self._getresponse("GET", url)

    def post(self, **kwargs):
        data = kwargs
        meta = dict([(k, data.pop(k)) for k in list(data.keys()) if k.startswith("__")])
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self._request("POST", self.url, data, headers, meta)
        return self._getresponse("POST", self.url, data, headers, meta)

    def put(self, **kwargs):
        if not self.id:
            return
        url = self.url + '/' + str(self.id)
        data = kwargs
        meta = dict([(k, data.pop(k)) for k in list(data.keys()) if k.startswith("__")])
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self._request("PUT", url, data, headers, meta)
        return self._getresponse("PUT", url, data, headers, meta)

    def delete(self, **kwargs):
        if not self.id:
            return
        url = self.url + '/' + str(self.id)
        self._request("DELETE", url, kwargs)
        return self._getresponse("DELETE", url, kwargs)

    def _request(self, method, url, data=None, headers=None, meta=None):
        pass

    def _getresponse(self, *args, **kwargs):
        return {"result": "dummy"}

    def __repr__(self):
        return "<Resource %s>" % (self.uri,)


class API(object):
    def __init__(self, base_url, auth=None):
        self.base_url = base_url
        self.auth = auth
        self.resources = {}

    def __getattr__(self, name):
        key = '/' + name
        self.resources[key] = Resource(uri=key, api=self)
        return self.resources[key]

    def __repr__(self):
        return "<API %s>" % self.base_url

def foo_not_supported():
    print('application/xml not supported yet!')