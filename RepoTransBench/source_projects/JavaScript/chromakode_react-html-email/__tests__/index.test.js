import * as mod from '../src/index.js';

describe('index.js exports', () => {
  it('exports main modules', () => {
    expect(mod.PropTypes).toBeDefined();
    expect(mod.configStyleValidator).toBeInstanceOf(Function);
    expect(mod.renderEmail).toBeInstanceOf(Function);
  });

  it('exports subcomponents', () => {
    expect(mod.Box).toBeDefined();
    expect(mod.Email).toBeDefined();
    expect(mod.Image).toBeDefined();
    expect(mod.Item).toBeDefined();
    expect(mod.Span).toBeDefined();
    expect(mod.A).toBeDefined();
  });

  it('exports default with keys', () => {
    expect(mod.default).toBeDefined();
    expect(mod.default.PropTypes).toBeDefined();
    expect(mod.default.configStyleValidator).toBeDefined();
    expect(mod.default.renderEmail).toBeDefined();
    expect(mod.default.styleValidator).toBeDefined();
  });
});