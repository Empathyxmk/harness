describe('examples/resourceful-app/app.js', () => {
  it('loads resourceful plugin and exposes app', () => {
    const app = require('../../examples/resourceful-app/app');
    expect(app).toBeDefined();
    // Further resourceful behavior would require HTTP server spin-up
    expect(app.plugins.resourceful).toBeDefined();
    expect(typeof app.plugins.resourceful).toBe('object');
  });
});