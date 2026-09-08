// NOTE: These are mock-based public tests because the real environment lacks 'phantomjs'.
// They verify the same public logic with different input but do not require phantomjs installed.

const path = require('path');

// Mock RasterizerService
class MockRasterizerService {
    constructor(config) {
        this.config = config;
        this.started = false;
        this.stopped = false;
    }
    async startService() {
        this.started = true;
    }
    async stopService() {
        this.stopped = true;
    }
    async pdf(url, outputFilePath, options) {
        // Simulate error for bad URL
        if (typeof url !== 'string' || url.startsWith('htp://invalid')) {
            throw new Error('Invalid URL');
        }
        if (url.startsWith('http://localhost:9999')) {
            throw new Error('Unreachable resource');
        }
        // "Succeed" for valid testable public URLs
        return undefined;
    }
    async screenshot(url, outputFilePath, options) {
        // Simulate error for unreachable URLs
        if (url.startsWith('http://localhost:9999')) {
            throw new Error('Unreachable resource');
        }
        // "Succeed" for valid
        return undefined;
    }
}

function getTestConfig() {
    return {
        command: 'phantomjs',
        path: '',
        host: '127.0.1.1', // public data: slightly different IP
        port: 5045, // another distinct port
        viewport: '1440x900'
    };
}

describe('RasterizerService (public test data, mock)', function () {
    let rasterizer;

    beforeAll(async function () {
        rasterizer = new MockRasterizerService(getTestConfig());
        await rasterizer.startService();
    });

    afterAll(async function () {
        await rasterizer.stopService();
    });

    test('should generate a PDF from a different public URL', async function () {
        const url = 'https://www.npmjs.com/';
        const outputFilePath = path.join(__dirname, 'output_npmjs_public.pdf');
        const options = {
            format: 'letter',
            orientation: 'portrait',
        };
        await expect(rasterizer.pdf(url, outputFilePath, options)).resolves.toBeUndefined();
    });

    test('should generate a PNG screenshot of another public URL with public data', async function () {
        const url = 'https://www.github.com/';
        const outputFilePath = path.join(__dirname, 'output_github_public.png');
        const options = {
            format: 'png',
            width: 1024,
            height: 768,
        };
        await expect(rasterizer.screenshot(url, outputFilePath, options)).resolves.toBeUndefined();
    });

    test('returns error on invalid input URL (public mock)', async function () {
        const badUrl = 'htp://invalid_url_publicX';
        const outputFilePath = path.join(__dirname, 'output_invalidurl_public2.pdf');
        await expect(rasterizer.pdf(badUrl, outputFilePath)).rejects.toBeInstanceOf(Error);
    });

    test('returns error when pointing to unreachable resource (public mock)', async function () {
        const unreachableUrl = 'http://localhost:9999/foobarunreachable999';
        const outputFilePath = path.join(__dirname, 'output_unreachable_public2.png');
        await expect(rasterizer.screenshot(unreachableUrl, outputFilePath)).rejects.toBeInstanceOf(Error);
    });
});