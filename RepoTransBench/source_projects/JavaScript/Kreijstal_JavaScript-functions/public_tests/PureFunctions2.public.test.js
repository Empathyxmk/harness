const {
  mapValueWithInstructions,
  stretchTileFunction,
  coordinatesToIndex,
  indexToCoordinates
} = require('../PureFunctions2');

describe('mapValueWithInstructions (public)', () => {
  it('swaps values with different numbers', () => {
    expect(mapValueWithInstructions(10, [10, 20], [20, 10])).toBe(20);
    expect(mapValueWithInstructions(20, [10, 20], [20, 10])).toBe(10);
    expect(mapValueWithInstructions(99, [10,20], [20,10])).toBe(99);
  });

  it('maps value for a different string match', () => {
    expect(
      mapValueWithInstructions(
        'searchThisString',
        ['containsThis','searchThisString'],
        ['output1','found value']
      )
    ).toBe('found value');
  });

  it('works with alternate finder and result functions', () => {
    const appleObj = { fruit: "apple" };
    const bananaObj = { fruit: "banana" };
    const result1 = mapValueWithInstructions(
      { fruit: "apple" },
      [
        a => a.fruit === "apple",
        a => a.fruit === "banana"
      ],
      [
        a => { a.fruit = "banana"; return a; },
        a => { a.fruit = "apple"; return a; }
      ]
    );
    expect(result1.fruit).toBe("banana");

    const result2 = mapValueWithInstructions(
      { fruit: "banana" },
      [
        a => a.fruit === "apple",
        a => a.fruit === "banana"
      ],
      [
        a => { a.fruit = "banana"; return a; },
        a => { a.fruit = "apple"; return a; }
      ]
    );
    expect(result2.fruit).toBe("apple");
  });

  it('returns original value if value not mapped', () => {
    expect(mapValueWithInstructions('absent', ['first','second'], [100,200])).toBe('absent');
  });
});

describe('stretchTileFunction (public)', () => {
  it('should call callback with different floored values', () => {
    const cb = jest.fn();
    const stretch = stretchTileFunction(cb, 3, 4);
    stretch(7,13);
    expect(cb).toBeCalledWith(2,3);
  });

  it('should return altered callback result', () => {
    const stretch = stretchTileFunction((x,y) => `B-${x}:${y}`, 4,5);
    expect(stretch(12,16)).toBe('B-3:3');
  });
});

describe('coordinatesToIndex (public)', () => {
  it('returns correct index for different 2D point', () => {
    expect(coordinatesToIndex(3, 2, 7)).toBe(17);
    expect(coordinatesToIndex(1, 0, 6)).toBe(1);
    expect(coordinatesToIndex(8, 4, 5)).toBe(8%5 + 4*5);
  });
});

describe('indexToCoordinates (public)', () => {
  it('returns correct x,y from different index values', () => {
    expect(indexToCoordinates(17, 7)).toEqual([3,2]);
    expect(indexToCoordinates(1, 6)).toEqual([1,0]);
    expect(indexToCoordinates(14, 5)).toEqual([4,2]);
  });
});