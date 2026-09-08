// Mocks must be put BEFORE require
jest.mock('blessed', () => {
  return {
    screen: jest.fn().mockReturnValue({
      on: jest.fn(),
      render: jest.fn(),
      key: jest.fn(),
      destroy: jest.fn(),
    }),
    box: jest.fn(() => ({})),
  };
}, {virtual: true});

jest.mock('blessed-contrib', () => {
  // Provide a dummy but *consistent* table instance structure
  const tableInstance = {
    focus: jest.fn(),
    setData: jest.fn(),
  };
  return {
    grid: jest.fn().mockReturnValue({
      set: jest.fn(() => {
        return tableInstance; // All set() calls return the actual instance with focus()
      }),
    }),
    donut: jest.fn(),
    line: jest.fn(),
    table: jest.fn(() => tableInstance),
    sparkline: jest.fn(),
  };
}, {virtual: true});

describe('gtop public', () => {
  it('requires without throwing (public)', () => {
    expect(() => {
      require('../../lib/gtop');
    }).not.toThrow();
  });
});