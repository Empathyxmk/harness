"""
Serialization helpers for JSON encoding/decoding Scrapy objects.
Patched to remove scrapy dependencies for testability.
"""

import json

# Dummy fallback for missing Scrapy types
class BaseItem(dict):
    pass

class Field(object):
    pass

class FakeSpider:
    name = "fakespider"

def is_item(obj):
    # Emulate Scrapy item check
    return isinstance(obj, (dict, BaseItem))

def _default(obj):
    # Handle custom serialization for items, fields, spiders, etc.
    if is_item(obj):
        return dict(obj)
    elif isinstance(obj, Field):
        return "<Field instance>"
    elif type(obj).__name__ == 'Spider':
        # Simulate spider
        return "<Spider: %s>" % getattr(obj, 'name', 'noname')
    raise TypeError("%r is not JSON serializable" % obj)

class ScrapyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return _default(obj)

class ScrapyJSONDecoder(json.JSONDecoder):
    # For now, simply default to stock decoder
    pass

def scrapy_json_dumps(obj):
    return json.dumps(obj, cls=ScrapyJSONEncoder)

def scrapy_json_loads(s):
    return json.loads(s, cls=ScrapyJSONDecoder)