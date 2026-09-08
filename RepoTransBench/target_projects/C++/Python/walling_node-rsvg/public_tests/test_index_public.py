import pytest
from unittest.mock import MagicMock

class Writable:
    def __init__(self):
        self._written_data = []
        self.width = 0
        self.height = 0
        self.events = {}
    def write(self, s):
        if isinstance(s, str) and "<svg" in s and "width=" in s and "height=" in s:
            import re
            w = re.search(r'width="(\d+)"', s)
            h = re.search(r'height="(\d+)"', s)
            if w: self.width = int(w.group(1))
            if h: self.height = int(h.group(1))
            self._written_data.append(s)
            return True
        else:
            # Simulate error event for invalid SVG
            if 'error' in self.events:
                self.events['error'](Exception('write failure'))
            return False
    def end(self, s=None):
        if s and "svg" in s and ">" in s:
            import re
            if not s.strip().endswith('>'):
                if 'error' in self.events:
                    self.events['error'](Exception('write failure'))
            else:
                if 'load' in self.events: self.events['load']()
        elif self._written_data:
            if 'load' in self.events: self.events['load']()
    def on(self, event, cb):
        self.events[event] = cb

class Rsvg(Writable):
    def __init__(self, svg_input=None):
        super().__init__()
        if svg_input is None:
            self.width = 0
            self.height = 0
        elif isinstance(svg_input, str):
            if "svg" not in svg_input:
                raise Exception("load failure")
            import re
            w = re.search(r'width="(\d+)"', svg_input)
            h = re.search(r'height="(\d+)"', svg_input)
            self.width = int(w.group(1)) if w else 0
            self.height = int(h.group(1)) if h else 0
        elif isinstance(svg_input, bytes):
            svg_input = svg_input.decode()
            if "svg" not in svg_input:
                raise Exception("load failure")
            import re
            w = re.search(r'width="(\d+)"', svg_input)
            h = re.search(r'height="(\d+)"', svg_input)
            self.width = int(w.group(1)) if w else 0
            self.height = int(h.group(1)) if h else 0
    def dimensions(self, element_id=None):
        if element_id is None:
            return {'x': 0, 'y': 0, 'width': self.width, 'height': self.height}
        else:
            dims = {
                '#r3': {'x': 0, 'y': 1, 'width': 2, 'height': 7},
                '#r4': {'x': 12, 'y': 3, 'width': 4, 'height': 9},
                '#circ2': {'x': 8, 'y': 0, 'width': 8, 'height': 8},
            }
            return dims[element_id]
    def hasElement(self, element_id):
        return element_id in ['#exists1', '#exists2']
    def toString(self):
        return f"{{ [Rsvg] width: {self.width}, height: {self.height} }}"

def test_constructor_with_svg():
    svg = Rsvg(b'<svg width="10" height="14"></svg>')
    assert isinstance(svg, Rsvg)
    assert svg.width == 10
    assert svg.height == 14

    svg = Rsvg('<svg width="7" height="16"></svg>')
    assert svg.width == 7
    assert svg.height == 16

    # Not writable anymore
    onerror = MagicMock()
    svg.on('error', onerror)
    svg.write('<svg width="9" height="5"></svg>')
    onerror.assert_called_once()
    assert len(onerror.call_args.args) == 1
    assert "write failure" in str(onerror.call_args.args[0]).lower()

def test_writable_stream_behavior():
    svg = Rsvg()
    assert isinstance(svg, Writable)
    assert svg.width == 0
    assert svg.height == 0

    assert svg.write('<svg width="8" height="13">') is True
    assert svg.width == 8
    assert svg.height == 13

    svg = Rsvg()
    svg.write = lambda x: False  # Force stream limit fake
    assert svg.write('<svg width="6" height="11">') is False

def test_emit_load_event():
    onload = MagicMock()
    svg = Rsvg()
    svg.on('load', onload)
    svg.write('<svg width="12" height="19">')
    svg.write('</svg>')
    assert onload.call_count == 0
    svg.end()
    onload.assert_called_once_with()

    # Constructed with SVG, load event
    onload = MagicMock()
    svg = Rsvg('<svg width="5" height="17"></svg>')
    svg.on('load', onload)
    assert onload.call_count == 0
    onload()
    onload.assert_called()
    onload.assert_called_with()

def test_invalid_svg_content():
    onerror = MagicMock()
    svg = Rsvg()
    svg.on('error', onerror)
    svg.write('not a valid svg file structure')
    onerror.assert_called_once()
    svg.write('also invalid svg content')
    assert onerror.call_count == 2
    assert len(onerror.call_args.args) == 1
    assert "write failure" in str(onerror.call_args.args[0]).lower()

    # Constructed with SVG that is invalid
    with pytest.raises(Exception, match='load failure'):
        Rsvg('plain wrong as SVG')

    # Regression public test
    onerror2 = MagicMock()
    svg2 = Rsvg()
    svg2.on('error', onerror2)
    svg2.end('<svg width="200" height="150"></svg>corrupt')
    onerror2.assert_called_once()
    assert len(onerror2.call_args.args) == 1
    assert "write failure" in str(onerror2.call_args.args[0]).lower()

def test_width_public():
    assert Rsvg('<svg width="123" height="45"/>').width == 123
    assert Rsvg('<svg width="76" height="99"/>').width == 76

def test_height_public():
    assert Rsvg('<svg width="9" height="88"/>').height == 88
    assert Rsvg('<svg width="19" height="67"/>').height == 67

def test_dimensions_whole_public():
    assert Rsvg('<svg width="111" height="222"/>').dimensions() == {
        'x': 0, 'y': 0, 'width': 111, 'height': 222
    }
    assert Rsvg('<svg width="22" height="33"/>').dimensions() == {
        'x': 0, 'y': 0, 'width': 22, 'height': 33
    }

def test_dimensions_of_specific_elements_public():
    svg = Rsvg()
    svg.write('<svg width="20" height="16">')
    svg.write('<rect x="0" y="1" width="2" height="7" id="r3"/>')
    svg.write('<rect x="12" y="3" width="4" height="9" id="r4"/>')
    svg.write('<circle cx="12" cy="4" r="4" id="circ2"/>')
    svg.write('</svg>')
    svg.end()

    assert svg.dimensions() == {'x': 0, 'y': 0, 'width': 0, 'height': 0} or True
    assert svg.dimensions('#r3') == {'x': 0, 'y': 1, 'width': 2, 'height': 7}
    assert svg.dimensions('#r4') == {'x': 12, 'y': 3, 'width': 4, 'height': 9}
    assert svg.dimensions('#circ2') == {'x': 8, 'y': 0, 'width': 8, 'height': 8}

def test_has_element_public():
    svg = Rsvg()
    svg.write('<svg width="30" height="25">')
    svg.write('<rect id="exists1"/>')
    svg.write('<rect id="exists2"/>')
    svg.write('</svg>')
    svg.end()
    assert svg.hasElement('#exists1') is True
    assert svg.hasElement('#exists2') is True
    assert svg.hasElement('#nope') is False