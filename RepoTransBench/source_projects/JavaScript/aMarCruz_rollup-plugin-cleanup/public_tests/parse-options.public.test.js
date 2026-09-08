import parseOptions from '../src/parse-options';

jest.mock('js-cleanup', () => jest.fn(() => undefined));

describe('parseOptions public tests', () => {
  const jsCleanup = require('js-cleanup');

  afterEach(() => {
    jsCleanup.mockClear();
  });

  it('returns correct defaults with unrelated options given', () => {
    const opts = parseOptions({ notARealOption: 123 });
    expect(opts).toEqual({
      comments: 'some',
      compactComments: true,
      lineEndings: undefined,
      maxEmptyLines: 0,
      sourcemap: true
    });
    expect(jsCleanup).not.toHaveBeenCalled();
  });

  it('handles comments as string values', () => {
    expect(parseOptions({ comments: 'none' }).comments).toBe('none');
    expect(parseOptions({ comments: 'all' }).comments).toBe('all');
  });

  it('normalizes comments array with other string and calls js-cleanup', () => {
    parseOptions({ comments: ['license'] });
    expect(jsCleanup).toHaveBeenCalledWith('', null, { comments: ['license'], sourcemap: false });
  });

  it('handles comments as a different array and calls js-cleanup', () => {
    parseOptions({ comments: ['copyright'] });
    expect(jsCleanup).toHaveBeenCalledWith('', null, { comments: ['copyright'], sourcemap: false });
  });

  it('propagates other options properly (different values)', () => {
    const opts = parseOptions({
      compactComments: true,
      lineEndings: '\r',
      maxEmptyLines: 2,
      sourceMap: false,
      sourcemap: false,
      comments: true
    });
    expect(opts.compactComments).toBe(true);
    expect(opts.lineEndings).toBe('\r');
    expect(opts.maxEmptyLines).toBe(2);
    expect(opts.sourcemap).toBe(false);
    expect(opts.comments).toBe('all');
  });

  it('handles both lineEndings and normalizeEols (different values)', () => {
    expect(parseOptions({ normalizeEols: '\n' }).lineEndings).toBe('\n');
    expect(parseOptions({ lineEndings: '\r\n' }).lineEndings).toBe('\r\n');
  });

  it('computes sourcemap as true if both sourceMap and sourcemap are true', () => {
    expect(parseOptions({ sourceMap: true, sourcemap: true }).sourcemap).toBe(true);
    expect(parseOptions({ sourcemap: true }).sourcemap).toBe(true);
  });
});