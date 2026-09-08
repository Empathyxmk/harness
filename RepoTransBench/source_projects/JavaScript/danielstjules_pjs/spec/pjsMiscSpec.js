const expect = require('expect.js');
const pjs = require('../lib/pjs.js');
const stream = require('stream');

describe('pjs.json', function() {
  it('outputs objects as JSON', function(done) {
    const data = [{a:1}, {b:2}];
    const s = new stream.Readable({objectMode: true, read() {
      this.push(data.shift());
      if (data.length === 0) this.push(null);
    }});
    const r = [];
    const jsonStream = pjs.json();
    jsonStream.on('data', d => r.push(d));
    jsonStream.on('end', () => {
      const combined = r.join('');
      expect(combined.includes('"a":1')).to.be(true);
      expect(combined.includes('"b":2')).to.be(true);
      done();
    });
    s.pipe(jsonStream);
  });
});

describe('pjs.ignore', function() {
  it('pass data through without modification', function(done) {
    const data = ['abc', 'def'];
    const s = new stream.Readable({objectMode: true, read() {
      this.push(data.shift());
      if (data.length === 0) this.push(null);
    }});
    const r = [];
    const ignoreStream = pjs.ignore();
    ignoreStream.on('data', d => r.push(d));
    ignoreStream.on('end', () => {
      expect(r).to.eql(['abc', 'def']);
      done();
    });
    s.pipe(ignoreStream);
  });
});