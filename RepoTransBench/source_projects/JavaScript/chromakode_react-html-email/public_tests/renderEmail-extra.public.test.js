import React from 'react';
import renderEmail from '../src/renderEmail';

describe('renderEmail (public)', () => {
  it('returns doctype + markup for different simple tree', () => {
    const Comp = () => <html><body><h2>Hello World!</h2></body></html>;
    const output = renderEmail(<Comp />);
    expect(output.startsWith('<!DOCTYPE html')).toBe(true);
    expect(output.indexOf('<h2>Hello World!</h2>')).toBeGreaterThan(0);
  });

  it('works with bare span element', () => {
    const output = renderEmail(<span />);
    expect(output).toContain('<span');
  });
});