const custom = require('../custom');

describe('custom.js (public)', () => {
  it('should return a transform stream function with alt env', () => {
    const fn = custom({ BAR: 'baz' });
    expect(typeof fn).toBe('function');
  });

  it('should handle completely empty env object', () => {
    const fn = custom(Object.create(null));
    expect(typeof fn).toBe('function');
  });

  it('should replace process.env variables in alternate source', (done) => {
    const env = { ALT_VAR: 'qux' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('qux');
      done();
    });
    stream.write('process.env.ALT_VAR');
    stream.end();
  });

  it('should leave untouched variables not present in env', (done) => {
    const env = { ALPHA: 'omega' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('process.env.BETA');
      done();
    });
    stream.write('process.env.BETA');
    stream.end();
  });

  it('should process multiple mixed env expressions', (done) => {
    const env = { FOO1: 'apple', FOO2: 'orange' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('apple');
      expect(result).toContain('orange');
      done();
    });
    stream.write('process.env.FOO1 + process.env.FOO2');
    stream.end();
  });
});