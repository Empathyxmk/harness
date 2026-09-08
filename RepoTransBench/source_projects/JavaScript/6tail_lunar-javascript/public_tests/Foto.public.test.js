const {Foto} = require('../lunar');

test('fromYmd() - public', () => {
  const foto = Foto.fromYmd(2019, 1, 1);
  expect(foto.getYear()).toBe(2019);
  expect(foto.getMonth()).toBe(1);
  expect(foto.getDay()).toBe(1);
  expect(typeof foto.toString()).toBe('string');
});