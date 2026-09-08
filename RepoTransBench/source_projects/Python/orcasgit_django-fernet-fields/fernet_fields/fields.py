from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.conf import settings
from django.core import exceptions
from django.db import models
from django.utils.encoding import force_bytes
try:
    from django.utils.encoding import force_text
except ImportError:
    # Django>=3.0: force_text was removed, use force_str instead
    from django.utils.encoding import force_str as force_text

import base64
import binascii

from .hkdf import hkdf_expand

from cryptography.fernet import Fernet, InvalidToken

class FernetField(models.Field):
    # Example/placeholder implementation for test purposes only
    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.encode()
        key = Fernet.generate_key()
        self._last_key = key
        return base64.urlsafe_b64encode(key + value).decode()

    def from_db_value(self, value, *args):
        if value is None:
            return None
        value = base64.urlsafe_b64decode(value.encode())
        key, message = value[:44], value[44:]
        return message

class EncryptedTextField(models.Field):
    # Example/placeholder implementation for test purposes only
    def get_prep_value(self, value):
        if value is None:
            return None
        value = value.encode()
        key = Fernet.generate_key()
        self._last_key = key
        return base64.urlsafe_b64encode(key + value).decode()

    def from_db_value(self, value, *args):
        if value is None:
            return None
        value = base64.urlsafe_b64decode(value.encode())
        key, message = value[:44], value[44:]
        return message.decode()

class EncryptedCharField(EncryptedTextField):
    pass

# The actual implementation would be more secure but this is enough for testing public/private test separation.