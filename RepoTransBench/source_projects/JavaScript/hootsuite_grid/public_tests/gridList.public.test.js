const path = require('path');
let GridList;
try {
  GridList = require('../src/gridList.js');
} catch (e) {
  // Try default export for ESM compatibility
  GridList = require('../src/gridList.js').default;
}

describe('GridList (public test)', () => {
  test('should initialize grid list with unique items and custom options', () => {
    const items = [
      {w: 2, h: 1, x: 1, y: 2},
      {w: 1, h: 2, x: 3, y: 1}
    ];
    const options = {lanes: 6, direction: 'vertical'};
    const grid = new GridList(items, options);
    expect(grid.items.length).toBe(2);
    expect(grid._options.lanes).toBe(6);
    expect(grid._options.direction).toBe('vertical');
  });

  test('should clone items with different values', () => {
    const items = [
      {w: 2, h: 2, x: 2, y: 3},
      {w: 3, h: 1, x: 0, y: 4}
    ];
    const cloned = GridList.cloneItems(items);
    expect(cloned).not.toBe(items);
    expect(cloned.length).toBe(2);
    expect(cloned[0]).toEqual(items[0]);
    expect(cloned[1]).toEqual(items[1]);
  });
});