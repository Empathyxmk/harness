const {
  mapValueWithInstructions,
  stretchTileFunction,
  coordinatesToIndex,
  indexToCoordinates
} = require('./PureFunctions2');

describe('mapValueWithInstructions', () => {
  it('swaps values according to sortOrder (simple numbers)', () => {
    expect(mapValueWithInstructions(1, [1,2], [2,1])).toBe(2);
    expect(mapValueWithInstructions(2, [1,2], [2,1])).toBe(1);
    expect(mapValueWithInstructions(3, [1,2], [2,1])).toBe(3);
  });

  it('returns mapped value for string match', () => {
    expect(
      mapValueWithInstructions(
        'findThisElement',
        ['in this list','findThisElement'],
        ['and replace it','with the index it found']
      )
    ).toBe('with the index it found');
  });

  it('works with finder functions and result functions', () => {
    const rockObj = { object: "rock" };
    const cloudObj = { object: "cloud" };
    const result1 = mapValueWithInstructions(
      { object: "rock" },
      [
        a => a.object === "rock",
        a => a.object === "cloud"
      ],
      [
        a => { a.object = "cloud"; return a; },
        a => { a.object = "rock"; return a; }
      ]
    );
    expect(result1.object).toBe("cloud");

    const result2 = mapValueWithInstructions(
      { object: "cloud" },
      [
        a => a.object === "rock",
        a => a.object === "cloud"
      ],
      [
        a => { a.object = "cloud"; return a; },
        a => { a.object = "rock"; return a; }
      ]
    );
    expect(result2.object).toBe("rock");
  });

  it('returns original value if not found', () => {
    expect(mapValueWithInstructions('nope', ['hello','world'], [1,2])).toBe('nope');
  });
});

describe('stretchTileFunction', () => {
  it('should call callback with floored values', () => {
    const cb = jest.fn();
    const stretch = stretchTileFunction(cb, 2, 3);
    stretch(5,8);
    expect(cb).toBeCalledWith(2,2);
  });

  it('should return callback result', () => {
    const stretch = stretchTileFunction((x,y) => `A-${x},${y}`, 2,2);
    expect(stretch(4,6)).toBe('A-2,3');
  });
});

describe('coordinatesToIndex', () => {
  it('returns correct index for 2D point', () => {
    expect(coordinatesToIndex(2, 1, 5)).toBe(7);
    expect(coordinatesToIndex(0, 0, 5)).toBe(0);
    expect(coordinatesToIndex(5, 2, 3)).toBe(5%3 + 2*3);
  });
});

describe('indexToCoordinates', () => {
  it('returns correct x,y from index', () => {
    expect(indexToCoordinates(7, 5)).toEqual([2,1]);
    expect(indexToCoordinates(0, 5)).toEqual([0,0]);
    expect(indexToCoordinates(8, 3)).toEqual([2,2]);
  });
});