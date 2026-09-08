import parseOptions from '../src/parse-options'

jest.mock('js-cleanup', () => jest.fn(() => undefined));

describe('parseOptions', () => {
  const jsCleanup = require('js-cleanup');

  afterEach(() => {
    jsCleanup.mockClear();
  });

  it('returns correct defaults when no options are provided', () => {
    const opts = parseOptions({});
    expect(opts).toEqual({
      comments: 'some',
      compactComments: true,
      lineEndings: undefined,
      maxEmptyLines: 0,
      sourcemap: true
    });
    expect(jsCleanup).not.toHaveBeenCalled();
  });

  it('handles comments as true/false', () => {
    expect(parseOptions({ comments: true }).comments).toBe('all');
    expect(parseOptions({ comments: false }).comments).toBe('none');
  });

  it('normalizes comments array and calls js-cleanup', () => {
    parseOptions({ comments: ['srcmaps'] });
    expect(jsCleanup).toHaveBeenCalledWith('', null, { comments: ['sources'], sourcemap: false });
  });

  it('normalizes comments string and calls js-cleanup', () => {
    parseOptions({ comments: 'sources' });
    expect(jsCleanup).toHaveBeenCalledWith('', null, { comments: ['sources'], sourcemap: false });
  });

  it('propagates other options properly', () => {
    const opts = parseOptions({
      compactComments: false,
      lineEndings: '\n',
      maxEmptyLines: 5,
      sourceMap: true,
      sourcemap: true,
      comments: false
    });
    expect(opts.compactComments).toBe(false);
    expect(opts.lineEndings).toBe('\n');
    expect(opts.maxEmptyLines).toBe(5);
    expect(opts.sourcemap).toBe(true);
    expect(opts.comments).toBe('none');
  });

  it('handles lineEndings and normalizeEols', () => {
    expect(parseOptions({ normalizeEols: '\r\n' }).lineEndings).toBe('\r\n');
    expect(parseOptions({ lineEndings: '\r' }).lineEndings).toBe('\r');
  });

  it('computes sourcemap as false if either sourceMap or sourcemap false', () => {
    expect(parseOptions({ sourceMap: false }).sourcemap).toBe(false);
    expect(parseOptions({ sourcemap: false }).sourcemap).toBe(false);
  });
});