/**
 * PUBLIC TEST for Editable Block (Different data)
 * - This test mocks the wp global as required by block.js
 * - Mocks registerBlockType so that the file loads for test
 */
const mockCreateElement = jest.fn();
const mockRegisterBlockType = jest.fn();
let editFn;

beforeAll(() => {
    // Setup a "wp" mock environment for block.js registration and block usage
    global.wp = {
        i18n: { __: (s) => s },
        element: {
            createElement: mockCreateElement,
        },
        blocks: {
            Editable: function Editable() {},
            source: { children: () => [] },
            registerBlockType: mockRegisterBlockType
        }
    };

    // Patch global scope for block.js
    global.registerBlockType = mockRegisterBlockType;

    // Dynamically load the block so it registers itself using our mocks
    jest.resetModules();
    require('./block.js');

    // Find the edit implementation that registerBlockType was called with
    // To do: Call edit for the block "gb/block-editable-03"
    let blockArgs = null;
    for (const call of mockRegisterBlockType.mock.calls) {
        if (call[0] === 'gb/block-editable-03') {
            blockArgs = call[1];
            break;
        }
    }
    if (!blockArgs) throw new Error('gb/block-editable-03 not registered');
    editFn = blockArgs.edit;
});

describe('gb/block-editable-03 Block (Public)', () => {
    beforeEach(() => {
        mockCreateElement.mockClear();
    });

    describe('edit renders "Editable" with default props & onChange', () => {
        it('should call createElement with alternate data (public)', () => {
            const defaultProps = {
                className: 'custom-public-class',
                value: 'test-value',
                // focus: true, // intentionally omitting focus
            };
            const onChange = jest.fn();
            editFn.call(
                {},
                {
                    className: defaultProps.className,
                    setAttributes: () => {},
                    attributes: {
                        content: defaultProps.value,
                        // focus: defaultProps.focus,
                    },
                    setFocus: () => {},
                    isSelected: true,
                    onChange,
                    editableRef: { current: null }
                }
            );
            expect(mockCreateElement).toHaveBeenCalled();
            const outProps = mockCreateElement.mock.calls[0][1];
            expect(outProps).toMatchObject({
                tagName: 'p',
                className: 'custom-public-class',
                value: 'test-value',
                // focus is not asserted here since it's omitted and (undefined)
            });
        });
    });

    describe('edit renders "Editable" with alternate props & onChange', () => {
        it('should call createElement with different data (public)', () => {
            const altProps = {
                className: 'alt-ed-public',
                value: 'gutenberg',
                // focus: false, // intentionally omitting focus
            };
            const onChange = jest.fn();
            editFn.call(
                {},
                {
                    className: altProps.className,
                    setAttributes: () => {},
                    attributes: {
                        content: altProps.value,
                        // focus: altProps.focus,
                    },
                    setFocus: () => {},
                    isSelected: false,
                    onChange,
                    editableRef: { current: null }
                }
            );
            expect(mockCreateElement).toHaveBeenCalled();
            const outProps = mockCreateElement.mock.calls[0][1];
            expect(outProps).toMatchObject({
                tagName: 'p',
                className: 'alt-ed-public',
                value: 'gutenberg',
                // focus is not asserted here
            });
        });
    });
});