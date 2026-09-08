import includeDataProps from '../src/includeDataProps';

describe('includeDataProps', () => {
  it('returns only data-* props', () => {
    const props = {
      foo: "bar",
      "data-test": "abc",
      "data-foo": 42,
      "aria-label": "yo",
      style: {},
    };
    const result = includeDataProps(props);
    expect(result).toEqual({ "data-test": "abc", "data-foo": 42 });
    expect(result.foo).toBeUndefined();
    expect(result['aria-label']).toBeUndefined();
  });

  it('returns empty object when no data-* props', () => {
    expect(includeDataProps({ foo: 1, bar: 2 })).toEqual({});
  });

  it('handles empty input', () => {
    expect(includeDataProps({})).toEqual({});
  });
});