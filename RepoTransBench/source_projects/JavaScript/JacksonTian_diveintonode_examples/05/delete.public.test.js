test('delete operator on object property (public)', () => {
  const obj = { alpha: 123, beta: 456 };
  expect('alpha' in obj).toBe(true);
  delete obj.alpha;
  expect(obj.alpha).toBeUndefined();
  expect('beta' in obj).toBe(true);
});
test('delete operator on array element (public)', () => {
  const arr = [10, 20, 30];
  delete arr[1];
  expect(arr[1]).toBeUndefined();
  expect(arr.length).toBe(3);
});