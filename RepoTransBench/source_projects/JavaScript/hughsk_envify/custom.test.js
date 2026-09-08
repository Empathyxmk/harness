const custom = require('./custom');

describe('custom.js', () => {
  it('should return a transform stream function when called', () => {
    const fn = custom({ FOO: 'bar' });
    expect(typeof fn).toBe('function');
  });

  it('should handle empty environment', () => {
    const fn = custom({});
    expect(typeof fn).toBe('function');
  });

  it('should replace process.env variables in source', (done) => {
    const env = { TEST_VAR: 'jsx' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('jsx');
      done();
    });
    stream.write('process.env.TEST_VAR');
    stream.end();
  });

  it('should skip variables not in env', (done) => {
    const env = { FOO: 'bar' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('process.env.BAZ');
      done();
    });
    stream.write('process.env.BAZ');
    stream.end();
  });

  it('should process mixed expressions', (done) => {
    const env = { X: '1', Y: '2' };
    const stream = custom(env)();
    let result = '';
    stream.on('data', chunk => { result += chunk; });
    stream.on('end', () => {
      expect(result).toContain('1');
      expect(result).toContain('2');
      done();
    });
    stream.write('process.env.X + process.env.Y');
    stream.end();
  });
});