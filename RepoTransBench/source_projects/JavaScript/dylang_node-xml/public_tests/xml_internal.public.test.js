// No original xml_internal.test.js provided, so copy structure with new keys
const xml = require('../lib/xml');

describe('xml internal (public basic)', () => {
  it('handles single object as xml (different keys)', () => {
    const str = xml({car: 'tesla'});
    expect(str).toBe('<car>tesla</car>');
  });
  it('handles deeply nested structure (different keys)', () => {
    const doc = {book: [{_attr: {lang: 'fr'}}, {title: 'Le Petit Prince'}]};
    const str = xml(doc);
    expect(str.includes('<book')).toBeTruthy();
    expect(str.includes('lang="fr"')).toBeTruthy();
    expect(str.includes('<title>Le Petit Prince</title>')).toBeTruthy();
  });
});