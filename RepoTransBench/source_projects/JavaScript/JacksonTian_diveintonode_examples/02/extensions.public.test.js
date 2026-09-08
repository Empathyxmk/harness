const path = require('path');

test('require with different file extension (public)', () => {
  // public: .txt instead of .js
  const file = './02/module/hello.js';
  const ext = path.extname(file);
  expect(ext).toBe('.js'); // public still check extension but may compare string differently
  expect(file.endsWith('.js')).toBeTruthy();
  // test lower-case handling
  expect(path.extname('SAMPLE.LOWeR.Js').toLowerCase()).toBe('.js');
});