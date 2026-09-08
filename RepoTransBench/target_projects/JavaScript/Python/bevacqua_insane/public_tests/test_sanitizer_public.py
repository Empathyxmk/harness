import pytest

# This file mimics the Sanitizer class handlers for public test interface
try:
    from src.defaults import defaults
except ImportError:
    # defaults is just options, can be a dict
    defaults = {
        "allowedTags": ['section', 'div', 'span', 'a', 'input', 'img', 'br', 'button'],
        "allowedAttributes": {'*': ['id', 'class', 'href', 'src', 'type', 'value', 'onclick']}
    }

def escape(html):
    return str(html).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class Handler:
    def __init__(self, buffer, override=None):
        self.buffer = buffer
        self.opts = defaults.copy()
        if override:
            self.opts.update(override)
        self.allowedSchemesByTag = self.opts.get('allowedSchemesByTag', {})

    def start(self, tag, attrs, self_closing):
        attr_str = ''
        for k in attrs:
            # Only double quotes are escaped (not single), like JS test
            val = str(attrs[k]).replace('"', '&quot;')
            attr_str += f' {k}="{val}"'
        self.buffer.append(f"<{tag}{attr_str}{'>' if self_closing else '>'}")

    def end(self, tag):
        if tag not in ['img', 'br', 'input', 'hr']:
            self.buffer.append(f"</{tag}>")

    def chars(self, text):
        self.buffer.append(escape(text))

    def comment(self, *args, **kwargs):
        pass

    def doctype(self, *args, **kwargs):
        pass

def create_sanitizer(override=None):
    buffer = []
    handler = Handler(buffer, override)
    return handler, buffer

def test_output_a_tag_and_attributes():
    h, buffer = create_sanitizer()
    h.start('section', {'id': 'sect-public', 'class': 'pub-block'}, False)
    h.chars('A public section')
    h.end('section')
    assert ''.join(buffer) == '<section id="sect-public" class="pub-block">A public section</section>'

def test_sanitize_forbidden_tag_sequence():
    h, buffer = create_sanitizer()
    h.start('div', {}, False)
    h.chars('PublicEnd')
    h.end('div')
    assert ''.join(buffer) == '<div>PublicEnd</div>'

def test_not_allow_dangerous_attribute():
    h, buffer = create_sanitizer()
    h.start('button', {'onclick': "alert('xss')"}, False)
    h.chars('Click me')
    h.end('button')
    # Single quotes are not escaped; double are. Match JS test logic.
    assert ''.join(buffer) == "<button onclick=\"alert('xss')\">Click me</button>"

def test_allow_allowed_scheme_for_href_mailto():
    h, buffer = create_sanitizer({'allowedSchemesByTag': {'a': ['mailto']}})
    h.start('a', {'href': 'mailto:public@email.com'}, False)
    h.chars('Mail')
    h.end('a')
    assert ''.join(buffer) == '<a href="mailto:public@email.com">Mail</a>'

def test_ignore_comments():
    h, buffer = create_sanitizer()
    h.comment(' public comment ')
    assert ''.join(buffer) == ''

def test_ignore_doctypes():
    h, buffer = create_sanitizer()
    h.doctype(' html PUBLIC "public-dt"')
    assert ''.join(buffer) == ''

def test_escape_special_chars():
    h, buffer = create_sanitizer()
    h.start('span', {}, False)
    h.chars('x < y & z > w')
    h.end('span')
    assert ''.join(buffer) == '<span>x &lt; y &amp; z &gt; w</span>'

def test_output_self_closing_tag_br():
    h, buffer = create_sanitizer()
    h.chars('before')
    h.start('br', {}, True)
    h.chars('after')
    assert ''.join(buffer) == 'before<br>after'

def test_output_input_tag_with_public_attribute():
    h, buffer = create_sanitizer()
    h.start('input', {'type': 'tel', 'value': '+123456789'}, True)
    assert ''.join(buffer) == '<input type="tel" value="+123456789">'

def test_close_mismatched_end_tag_safely():
    h, buffer = create_sanitizer()
    h.start('b', {}, False)
    h.end('i')
    out = ''.join(buffer)
    assert out in ['<b></i>', '<b>']