describe('src/index.js (public)', () => {
  it('should run without throwing an error when required', () => {
    expect(() => { require('../src/index.js'); }).not.toThrow();
  });

  it('should define document and window when running (if in jsdom)', () => {
    expect(typeof window).toBe('object');
    expect(typeof document).toBe('object');
  });
});