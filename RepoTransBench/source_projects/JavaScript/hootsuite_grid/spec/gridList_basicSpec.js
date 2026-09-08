const GridList = require('../src/gridList.js');

describe('GridList Basic Functionality', () => {
  it('should use default options if none supplied', () => {
    const items = [{w: 1, h: 1, x: 0, y: 0}];
    const grid = new GridList(items, {});
    expect(grid._options.lanes).toBe(5);
    expect(grid._options.direction).toBe('horizontal');
  });

  it('should set options from constructor', () => {
    const items = [{w: 1, h: 1, x: 0, y: 0}];
    const grid = new GridList(items, {lanes: 2, direction: 'vertical'});
    expect(grid._options.lanes).toBe(2);
    expect(grid._options.direction).toBe('vertical');
  });

  it('should deeply clone items', () => {
    const items = [
      {w: 2, h: 1, x: 0, y: 0, foo: 'bar'},
      {w: 1, h: 2, x: 2, y: 0, bar: 'baz'}
    ];
    const clone = GridList.cloneItems(items);
    expect(clone).not.toBe(items);
    expect(clone[0]).not.toBe(items[0]);
    expect(clone[1]).not.toBe(items[1]);
    expect(clone).toEqual(items);
  });

  it('should produce correct string output from toString()', () => {
    const items = [
      {w: 1, h: 1, x: 0, y: 0},
      {w: 1, h: 1, x: 1, y: 0},
      {w: 1, h: 1, x: 0, y: 1},
    ];
    const grid = new GridList(items, {lanes: 2});
    const str = grid.toString();
    expect(typeof str).toBe('string');
    expect(str).toMatch(/0\|/); // header
    expect(str).toMatch(/--/);  // empty slot rendering
  });
});