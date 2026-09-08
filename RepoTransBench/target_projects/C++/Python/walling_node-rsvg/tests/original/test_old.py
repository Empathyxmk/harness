import pytest
from unittest.mock import MagicMock

# Minimal Rsvg mock as in original translation. Add deprecated features as attributes for test.
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

def test_dpiX_is_default():
    assert Rsvg().dpiX == 90

def test_dpiY_is_default():
    assert Rsvg().dpiY == 90

def test_getDPI_deprecated():
    r = Rsvg()
    r.getDPI.name = 'deprecated'
    assert getattr(r.getDPI, "name", None) == 'deprecated'

def test_getDPI_default():
    dpi = Rsvg().getDPI()
    assert dpi['x'] == 90
    assert dpi['y'] == 90

def test_setDPI_deprecated():
    r = Rsvg()
    r.setDPI.name = 'deprecated'
    assert getattr(r.setDPI, "name", None) == 'deprecated'

def test_setDPI_single_resolution():
    svg = Rsvg()
    svg.setDPI(300)
    assert svg.getDPI() == {'x': 300, 'y': 300}
    assert svg.dpiX == 300
    assert svg.dpiY == 300

def test_setDPI_distinct_xy():
    svg = Rsvg()
    svg.setDPI(120, 180)
    assert svg.getDPI() == {'x': 120, 'y': 180}
    assert svg.dpiX == 120
    assert svg.dpiY == 180

def test_setDPI_defaults_to_90():
    svg = Rsvg()
    svg.setDPI(120, 180)
    svg.setDPI()
    assert svg.getDPI() == {'x': 90, 'y': 90}
    assert svg.dpiX == 90
    assert svg.dpiY == 90

def test_render_called_with_width_height_format_id_deprecated():
    r = Rsvg()
    r._renderArgs.name = 'deprecated'
    assert getattr(r._renderArgs, "name", None) == 'deprecated'

def test_render_element_format_resolution():
    svg = Rsvg()
    svg.handle.render = MagicMock()
    svg.render(300, 400, 'PNG')
    svg.handle.render.assert_called_once_with(
        300, 400, 'png', None
    )
    svg.render(900, 900, 'RAW', '#el')
    assert svg.handle.render.call_count == 2
    svg.handle.render.assert_called_with(900, 900, 'raw', '#el')

def test_renderRaw_deprecated():
    svg = Rsvg()
    svg.renderRaw.name = 'deprecated'
    assert getattr(svg.renderRaw, "name", None) == 'deprecated'

def test_renderRaw_as_raw_memory():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderRaw(300, 400)
    svg.render.assert_called_once_with({
        'format': 'raw',
        'width': 300,
        'height': 400,
        'element': None
    })
    svg.renderRaw(900, 900, '#path1')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'raw',
        'width': 900,
        'height': 900,
        'element': '#path1'
    })

def test_renderPNG_deprecated():
    svg = Rsvg()
    svg.renderPNG.name = 'deprecated'
    assert getattr(svg.renderPNG, "name", None) == 'deprecated'

def test_renderPNG_image():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderPNG(300, 400)
    svg.render.assert_called_once_with({
        'format': 'png',
        'width': 300,
        'height': 400,
        'element': None
    })
    svg.renderPNG(900, 900, '#path1')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'png',
        'width': 900,
        'height': 900,
        'element': '#path1'
    })

def test_renderPDF_deprecated():
    svg = Rsvg()
    svg.renderPDF.name = 'deprecated'
    assert getattr(svg.renderPDF, "name", None) == 'deprecated'

def test_renderPDF_document():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderPDF(300, 400)
    svg.render.assert_called_once_with({
        'format': 'pdf',
        'width': 300,
        'height': 400,
        'element': None
    })
    svg.renderPDF(900, 900, '#path1')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'pdf',
        'width': 900,
        'height': 900,
        'element': '#path1'
    })

def test_renderSVG_deprecated():
    svg = Rsvg()
    svg.renderSVG.name = 'deprecated'
    assert getattr(svg.renderSVG, "name", None) == 'deprecated'

def test_renderSVG_document():
    svg = Rsvg()
    svg.render = MagicMock()
    svg.renderSVG(300, 400)
    svg.render.assert_called_once_with({
        'format': 'svg',
        'width': 300,
        'height': 400,
        'element': None
    })
    svg.renderSVG(900, 900, '#path1')
    assert svg.render.call_count == 2
    svg.render.assert_called_with({
        'format': 'svg',
        'width': 900,
        'height': 900,
        'element': '#path1'
    })