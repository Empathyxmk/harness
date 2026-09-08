import urllib.parse
import xml.etree.ElementTree as ET
import datetime

def escape_path(path):
    return urllib.parse.quote(path, safe="/")

def unescape_path(path):
    return urllib.parse.unquote(path)

def to_unicode(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value

def to_bytes(value):
    if isinstance(value, bytes):
        return value
    return value.encode("utf-8")

def strip_trailing_slash(path):
    if path and path != "/" and path.endswith("/"):
        return path[:-1]
    return path

class ResponseError(Exception):
    def __init__(self, response_or_code, msg=None):
        self._resource_body = None
        if isinstance(response_or_code, int):
            self.status_code = response_or_code
            text = ""
            if msg:
                error_msg = f"{msg} error: {self.status_code}"
            else:
                error_msg = f"HTTP error: {self.status_code}"
        else:
            self.status_code = getattr(response_or_code, 'status_code', None)
            content = getattr(response_or_code, 'content', None)
            self._resource_body = content
            if isinstance(content, bytes):
                try:
                    text = content.decode("utf-8")
                except Exception:
                    text = str(content)
            elif isinstance(content, str):
                text = content
            elif isinstance(content, list) and len(content) > 0:
                text = str(content[0])
            else:
                text = ""
            error_msg = f"HTTP error: {self.status_code}"
            if msg:
                error_msg += f" ({msg})"
            if text:
                error_msg += f" - {text}"
        super().__init__(error_msg)

    def get_resource_body(self):
        return self._resource_body

class HTTPResponseError(ResponseError):
    pass

class OCSResponseError(Exception):
    def __init__(self, response):
        self.res = response
        self.message = "OCS response error"
        self.status_code = getattr(response, "status_code", None)
        self.content = getattr(response, "content", [b""])
        text = ""
        xml_str = ""
        content = self.content
        if isinstance(content, (bytes, str)):
            xml_str = content
        elif isinstance(content, list) and content:
            xml_str = content[0]
        if isinstance(xml_str, bytes):
            try:
                xml_str = xml_str.decode("utf-8")
            except Exception:
                xml_str = str(xml_str)
        try:
            root = ET.fromstring(xml_str)
            msg_tag = root.find(".//message")
            if msg_tag is not None and msg_tag.text:
                text = msg_tag.text
        except Exception:
            text = ""
        if text:
            self.message += f": {text}"
        super().__init__(self.message)

    def get_resource_body(self):
        if self.res is None:
            return None
        return getattr(self.res, "content", None)

class ShareInfo:
    _remove = ('token', 'url', 'item_type', 'item_source', 'file_source', 'parent', 'other', 'storage', 'mail_send', 'stime')

    def __init__(self, info_dict):
        self._attrs = {}
        for key, value in info_dict.items():
            v = value
            try:
                if isinstance(v, str) and v.isdigit():
                    v = int(v)
            except Exception:
                pass
            setattr(self, key, v)
            self._attrs[key] = v

    def del_attrs(self):
        for rem in self._remove:
            if hasattr(self, rem):
                delattr(self, rem)
            if rem in self._attrs:
                self._attrs.pop(rem)
        core = {"id", "share_type", "permissions", "expiration"}
        keys_to_remove = [k for k in list(self._attrs) if k not in core]
        for k in keys_to_remove:
            self._attrs.pop(k)

    def get_id(self):
        return self._attrs.get("id")

    def get_share_type(self):
        return self._attrs.get("share_type")

    def get_permissions(self):
        return self._attrs.get("permissions")

    def get_expiration(self):
        return self._attrs.get("expiration")

    def get_token(self):
        return self._attrs.get("token", None)

    def get_share_with(self):
        return self._attrs.get("share_with")

    def get_share_with_displayname(self):
        return self._attrs.get("share_with_displayname")

    def get_share_time(self):
        stime = self._attrs.get("stime")
        if stime is None:
            return None
        try:
            # support both int/float and string that can be parsed as timestamp
            val = int(stime)
            # attempt to return a datetime for compatibility with some test code
            try:
                return datetime.datetime.fromtimestamp(val)
            except Exception:
                return val
        except Exception:
            return None

    def get_path(self):
        return self._attrs.get("path")

    def _get_int(self, item):
        val = self._attrs.get(item)
        if val is None:
            return None
        try:
            return int(val)
        except Exception:
            return None

    def __contains__(self, item):
        return item in self._attrs

    def __getitem__(self, item):
        return self._attrs[item]

    @property
    def share_info(self):
        return self._attrs