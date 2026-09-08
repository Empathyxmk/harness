const xml = require('../lib/xml');

describe('xml main API (public)', () => {
  it('outputs as a stream with stream:true (different tag/value)', done => {
    const elem = xml.Element({animal: 'cat'});
    const stream = xml({zoo: elem}, {stream: true});
    let results = [];
    stream.on('data', chunk => results.push(chunk));
    stream.on('end', () => {
      const joined = results.join('');
      // Accept both possible outputs as in original, but for new structure
      if (!/<animal>cat<\/animal>/.test(joined)) {
        expect(joined).toBe('<zoo></zoo>');
      } else {
        expect(joined).toContain('<animal>cat</animal>');
        expect(joined).toContain('<zoo>');
      }
      done();
    });
    elem.close();
  });
});