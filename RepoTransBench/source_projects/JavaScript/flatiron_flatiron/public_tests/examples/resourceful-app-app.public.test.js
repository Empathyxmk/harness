describe('examples/resourceful-app/app.js [public]', () => {
  it('exposes app and has resourceful plugin (public)', () => {
    const app = require('../../examples/resourceful-app/app');
    expect(app).not.toBeNull();
    expect(app.plugins).not.toBeNull();
    expect(Object.keys(app.plugins)).toContain('resourceful');
    expect(typeof app.plugins.resourceful).not.toBe('undefined');
  });
});