import includeDataProps from '../src/includeDataProps';

describe('includeDataProps (public)', () => {
  it('returns only data-* props with different inputs', () => {
    const props = {
      hello: "world",
      "data-public": "xyz",
      "data-bar": 123,
      "aria-hidden": "false",
      className: "my-class",
    };
    const result = includeDataProps(props);
    expect(result).toEqual({ "data-public": "xyz", "data-bar": 123 });
    expect(result.hello).toBeUndefined();
    expect(result['aria-hidden']).toBeUndefined();
  });

  it('returns empty object when there are only non-data props', () => {
    expect(includeDataProps({ alpha: 7, bravo: 'zulu' })).toEqual({});
  });

  it('handles empty input (public)', () => {
    expect(includeDataProps({})).toEqual({});
  });
});