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
        # Simulate error for bad URL
        if not isinstance(url, str) or url.startswith('htp://invalid'):
            raise ValueError('Invalid URL')
        if url.startswith('http://localhost:9999'):
            raise ValueError('Unreachable resource')
        return None

    async def screenshot(self, url, outputFilePath, options=None):
        if url.startswith('http://localhost:9999'):
            raise ValueError('Unreachable resource')
        return None

def getTestConfig():
    return {
        'command': 'phantomjs',
        'path': '',
        'host': '127.0.1.1', # public data: slightly different IP
        'port': 5045, # another distinct port
        'viewport': '1440x900'
    }

import asyncio

@pytest.mark.asyncio
class TestRasterizerServicePublic:
    @classmethod
    def setup_class(cls):
        cls.rasterizer = MockRasterizerService(getTestConfig())
        asyncio.get_event_loop().run_until_complete(cls.rasterizer.startService())

    @classmethod
    def teardown_class(cls):
        asyncio.get_event_loop().run_until_complete(cls.rasterizer.stopService())

    @pytest.mark.asyncio
    async def test_should_generate_pdf_from_different_public_url(self):
        url = 'https://www.npmjs.com/'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_npmjs_public.pdf')
        options = {
            'format': 'letter',
            'orientation': 'portrait'
        }
        result = await self.rasterizer.pdf(url, outputFilePath, options)
        assert result is None

    @pytest.mark.asyncio
    async def test_should_generate_png_screenshot_public(self):
        url = 'https://www.github.com/'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_github_public.png')
        options = {
            'format': 'png',
            'width': 1024,
            'height': 768
        }
        result = await self.rasterizer.screenshot(url, outputFilePath, options)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_error_on_invalid_input_url_public(self):
        badUrl = 'htp://invalid_url_publicX'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_invalidurl_public2.pdf')
        with pytest.raises(ValueError) as excinfo:
            await self.rasterizer.pdf(badUrl, outputFilePath)
        assert 'Invalid URL' in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_returns_error_when_pointing_to_unreachable_resource_public(self):
        unreachableUrl = 'http://localhost:9999/foobarunreachable999'
        outputFilePath = os.path.join(os.path.dirname(__file__), 'output_unreachable_public2.png')
        with pytest.raises(ValueError) as excinfo:
            await self.rasterizer.screenshot(unreachableUrl, outputFilePath)
        assert 'Unreachable resource' in str(excinfo.value)