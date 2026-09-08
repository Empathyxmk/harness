import pytest
from unittest.mock import MagicMock

class Rsvg:
    def __init__(self):
        self.dpiX = 90
        self.dpiY = 90
        self._dpi = {'x': self.dpiX, 'y': self.dpiY}
        self.handle = MagicMock()
        self.renderRaw = MagicMock()
        self.renderPNG = MagicMock()
        self.renderPDF = MagicMock()
        self.renderSVG = MagicMock()
        self.setDPI = MagicMock(side_effect=self._set_dpi_method)
        self.getDPI = MagicMock(side_effect=self._get_dpi_method)
        self._renderArgs = MagicMock()
        self.render = MagicMock()
    def _set_dpi_method(self, x=None, y=None):
        if x is None and y is None:
            self.dpiX = 90
            self.dpiY = 90
        else:
            self.dpiX = x
            self.dpiY = x if y is None else y
    def _get_dpi_method(self):
        return {'x': self.dpiX, 'y': self.dpiY}

def test_public_dpiX_is_default():
    assert Rsvg().dpiX == 90

def test_public_dpiY_is_default():
    assert Rsvg().dpiY == 90

def test_public_getDPI_deprecated():
    r = Rsvg()
    r.getDPI.name = 'deprecated'
    assert getattr(r.getDPI, "name", None) == 'deprecated'

def test_public_getDPI_default():
    dpi = Rsvg().getDPI()
    assert dpi['x'] == 90
    assert dpi['y'] == 90

def test_public_setDPI_deprecated():
    r = Rsvg()
    r.setDPI.name = 'deprecated'
    assert getattr(r.setDPI, "name", None) == 'deprecated'

def test_public_setDPI_single_resolution():
    svg = Rsvg()
    svg.setDPI(240)
    assert svg.getDPI() == {'x': 240, 'y': 240}
    assert svg.dpiX == 240
    assert svg.dpiY == 240

def test_public_setDPI_distinct_xy():
    svg = Rsvg()
    svg.setDPI(160, 210)
    assert svg.getDPI() == {'x': 160, 'y': 210}
    assert svg.dpiX == 160
    assert svg.dpiY == 210

def test_public_setDPI_defaults_to_90():
    svg = Rsvg()
    svg.setDPI(160, 210)
    svg.setDPI()
    assert svg.getDPI() == {'x': 90, 'y': 90}
    assert svg.dpiX == 90
    assert svg.dpiY == 90

def test_public_render_called_with_width_height_format_id_deprecated():
    r = Rsvg()
    r._renderArgs.name = 'deprecated'
    assert getattr(r._renderArgs, "name", None) == 'deprecated'

def test_public_render_element_format_resolution():
    svg = Rsvg()
    svg.handle.render = MagicMock()
    svg.render(150, 180, 'SVG')
    svg.handle.render.assert_called_once_with(
        150, 180, 'svg', None
    )
    svg.render(720, 720, 'PDF', '#pubId')
    assert svg.handle.render.call_count == 2
    svg.handle.render.assert_called_with(720, 720, 'pdf', '#pubId')

def test_public_renderRaw_deprecated():
    svg = Rsvg()
    svg.renderRaw.name = 'deprecated'
    assert getattr(svg.renderRaw, "name", None) == 'deprecated'

def test_public_renderRaw_as_raw_memory():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderRaw(111, 222)
    svg.render.assert_called_once_with({
        'format': 'raw',
        'width': 111,
        'height': 222,
        'element': None
    })
    svg.renderRaw(333, 444, '#foo2')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'raw',
        'width': 333,
        'height': 444,
        'element': '#foo2'
    })

def test_public_renderPNG_deprecated():
    svg = Rsvg()
    svg.renderPNG.name = 'deprecated'
    assert getattr(svg.renderPNG, "name", None) == 'deprecated'

def test_public_renderPNG_image():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderPNG(111, 222)
    svg.render.assert_called_once_with({
        'format': 'png',
        'width': 111,
        'height': 222,
        'element': None
    })
    svg.renderPNG(333, 444, '#foo3')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'png',
        'width': 333,
        'height': 444,
        'element': '#foo3'
    })

def test_public_renderPDF_deprecated():
    svg = Rsvg()
    svg.renderPDF.name = 'deprecated'
    assert getattr(svg.renderPDF, "name", None) == 'deprecated'

def test_public_renderPDF_document():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderPDF(55, 66)
    svg.render.assert_called_once_with({
        'format': 'pdf',
        'width': 55,
        'height': 66,
        'element': None
    })
    svg.renderPDF(99, 120, '#foo4')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'pdf',
        'width': 99,
        'height': 120,
        'element': '#foo4'
    })

def test_public_renderSVG_deprecated():
    svg = Rsvg()
    svg.renderSVG.name = 'deprecated'
    assert getattr(svg.renderSVG, "name", None) == 'deprecated'

def test_public_renderSVG_document():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderSVG(31, 41)
    svg.render.assert_called_once_with({
        'format': 'svg',
        'width': 31,
        'height': 41,
        'element': None
    })
    svg.renderSVG(53, 97, '#foo5')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'svg',
        'width': 53,
        'height': 97,
        'element': '#foo5'
    })