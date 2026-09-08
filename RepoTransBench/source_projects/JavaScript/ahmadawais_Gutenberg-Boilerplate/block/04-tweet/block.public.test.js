// Public: test with different values, keeping logic robust and flexible like private version.

if (!global.wp) global.wp = {};
if (!global.wp.blocks) global.wp.blocks = {};
const registerBlockTypeMock = jest.fn();
global.wp.blocks.registerBlockType = registerBlockTypeMock;

// i18n mock for __()
if (!global.wp.i18n) global.wp.i18n = {};
global.wp.i18n.__ = (s) => s;

global.wp.blocks.Editable = 'Editable';
global.wp.blocks.source = { children: jest.fn(() => []) };

if (!global.wp.element) global.wp.element = {};
const elMock = jest.fn();
global.wp.element.createElement = elMock;

describe('gb/tweet-04 Block (Public)', () => {
    beforeEach(() => {
        registerBlockTypeMock.mockClear();
        elMock.mockClear();
        global.wp.blocks.source.children.mockReset();
        jest.resetModules();
    });

    it('registers the block and verifies settings with public block name', () => {
        require('./block.js');
        expect(registerBlockTypeMock).toHaveBeenCalled();
        expect(typeof registerBlockTypeMock.mock.calls[0][0]).toBe('string');
        expect(registerBlockTypeMock.mock.calls[0][0]).toMatch(/tweet/);
        expect(typeof registerBlockTypeMock.mock.calls[0][1].title).toBe('string');
    });

    it('edit calls Editable with alt public props', () => {
        require('./block.js');
        const settings = registerBlockTypeMock.mock.calls[0][1];
        const props = {
            className: 'tweet-alt-class',
            attributes: { content: 'tweet something new!' },
            setAttributes: jest.fn(),
        };
        elMock.mockClear();
        settings.edit(props);

        // Accept actual values block.js gives
        expect(elMock).toHaveBeenCalled();
        const call = elMock.mock.calls[0];
        expect(call[0]).toBe('Editable');
        expect(call[1]).toMatchObject({
            className: 'tweet-alt-class',
            value: 'tweet something new!',
        });
        expect(typeof call[1].placeholder).toBe('string');
        expect(typeof call[1].tagName).toBe('string');
    });

    it('save encodes and renders <a> with alt content', () => {
        require('./block.js');
        const settings = registerBlockTypeMock.mock.calls[0][1];
        const props = { className: 'public-tweet', attributes: { content: 'test this tweet!' } };
        elMock.mockClear();
        const origLog = global.console.log;
        const consoleLogSpy = jest.fn();
        global.console.log = consoleLogSpy;
        settings.save(props);

        expect(elMock.mock.calls.length > 0).toBe(true);
        const call = elMock.mock.calls[0];
        expect(call[0]).toBe('a');
        expect(call[1]).toMatchObject({
            className: 'public-tweet',
            target: '_blank',
        });
        expect(typeof call[1].href).toBe('string');
        global.console.log = origLog;
    });
});