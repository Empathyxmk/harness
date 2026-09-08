// Move EventEmitter require *inside* the jest.mock factory to comply with Jest restrictions
jest.mock('../lib/discovery', () => {
  const { EventEmitter } = require('events');
  return {
    Devices: jest.fn().mockImplementation(({ filter }) => {
      const e = new EventEmitter();
      setTimeout(() => {
        const dev = {id: '1', metadata: { types: new Set(['miio:type']), capabilities: new Set(['cap'])}, management: { address: 'x', model: 'm'}};
        if (!filter || filter(dev)) e.emit('available', dev);
        e.emit('unavailable', dev);
      }, 10);
      return e;
    })
  };
});
jest.mock('../lib/connectToDevice', () => jest.fn((opts) => {
  return opts.address === '1.2.3.4'
    ? Promise.resolve({id:'x'})
    : Promise.reject('fail');
}));

const deviceFinder = require('./device-finder');

describe('cli/device-finder', () => {
  it('should connect directly if given an IP filter', done => {
    const events = [];
    const finder = deviceFinder({filter: '1.2.3.4'});
    finder.on('available', device => {
      expect(device).toEqual({id: 'x'});
      events.push('available');
    });
    finder.on('done', () => {
      events.push('done');
      // Accept ['available', 'done'] order
      expect(events).toEqual(['available', 'done']);
      done();
    });
    setTimeout(() => { finder.emit('done') }, 30);
  });

  it('should browse and filter by string', done => {
    const finder = deviceFinder({filter: '1'});
    finder.on('available', device => {
      expect(device.id).toBe('1');
      done();
    });
  });

  it('should browse with no filter', done => {
    const finder = deviceFinder({});
    finder.on('available', device => {
      expect(device).toBeDefined();
      done();
    });
  });

  it('should allow function filter', done => {
    const filterFn = jest.fn().mockReturnValue(true);
    const finder = deviceFinder({filter: filterFn});
    finder.on('available', device => {
      expect(filterFn).toBeCalled();
      done();
    });
  });

  it('should trigger on unavailable', done => {
    const finder = deviceFinder({});
    finder.on('unavailable', device => {
      expect(device).toBeDefined();
      done();
    });
  });
});