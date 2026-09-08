import React from 'react';
import renderEmail from '../src/renderEmail';

describe('renderEmail', () => {
  it('returns doctype + markup for simple tree', () => {
    const Comp = () => <html><body><h1>Hi!</h1></body></html>;
    const output = renderEmail(<Comp />);
    expect(output.startsWith('<!DOCTYPE html')).toBe(true);
    expect(output.indexOf('<h1>Hi!</h1>')).toBeGreaterThan(0);
  });

  it('works with bare div', () => {
    const output = renderEmail(<div />);
    expect(output).toContain('<div');
  });
});