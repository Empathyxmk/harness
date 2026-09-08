const { Solar } = require("../lunar");

// Fix: Check Solar.toYmd() return type for real implementation
describe('Solar Public API', () => {
  test('Solar.toYmd returns correct day as string', () => {
    const s = Solar.fromYmd(2020, 2, 2);
    expect(s.toYmd()).toBe("2020-02-02");
  });

  test('Solar.next and prev days', () => {
    const s = Solar.fromYmd(2020, 2, 2);
    const next = s.next(1);
    expect(next.getDay()).toBe(3);
    const prev = s.next(-1);
    expect(prev.getDay()).toBe(1);
  });
});