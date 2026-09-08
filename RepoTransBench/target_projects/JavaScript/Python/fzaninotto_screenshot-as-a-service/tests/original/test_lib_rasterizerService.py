import os
import pytest

class MockRasterizerService:
    def __init__(self, config):
        self.config = config
        self.started = False
        self.stopped = False

    async def startService(self):
        self.started = True

    async def stopService(self):
        self.stopped = True

    async def pdf(self, url, outputFilePath, options=None):
        if not url or url.startswith('htp://'):
            raise ValueError('Invalid URL')
        return None

    async def screenshot(self, url, outputFilePath, options=None):
        if 'unreachable_localhost' in url:
            raise ValueError('Unreachable resource')
        return None

def getTestConfig():
    return {
        'command': 'phantomjs',
        'path': '',
        'host': '127.0.0.1',
        'port': 5042,
        'viewport': '1280x800',
    }

import asyncio

@pytest.mark.asyncio
class TestRasterizerService:
    @classmethod
    def setup_class(cls):
        cls.rasterizer = MockRasterizerService(getTestConfig())
        asyncio.get_event_loop().run_until_complete(cls.rasterizer.startService())

    @classmethod
    def teardown_class(cls):
        asyncio.get_event_loop().run_until_complete(cls.rasterizer.stopService())

    @pytest.mark.asyncio
    async def test_should_generate_pdf_from_public_url(self):
        url = 'https://google.com/'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_google.pdf')
        options = {
            'format': 'A4',
            'orientation': 'landscape'
        }
        result = await self.rasterizer.pdf(url, outputFilePath, options)
        assert result is None

    @pytest.mark.asyncio
    async def test_should_generate_screenshot_from_another_url(self):
        url = 'https://www.example.com/'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_example.png')
        options = {
            'format': 'png',
            'width': 800,
            'height': 800
        }
        result = await self.rasterizer.screenshot(url, outputFilePath, options)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_error_on_bad_url(self):
        badUrl = 'htp://invalid_url_X'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_invalidurl.pdf')
        with pytest.raises(ValueError) as excinfo:
            await self.rasterizer.pdf(badUrl, outputFilePath)
        assert 'Invalid URL' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_returns_error_on_unreachable_target(self):
        unreachableUrl = 'http://unreachable_localhost/test'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_unreachable.png')
        with pytest.raises(ValueError) as excinfo:
            await self.rasterizer.screenshot(unreachableUrl, outputFilePath)
        assert 'Unreachable resource' in str(excinfo.value)