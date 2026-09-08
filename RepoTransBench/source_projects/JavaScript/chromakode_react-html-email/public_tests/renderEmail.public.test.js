import React from 'react';
import renderEmail from '../src/renderEmail';

describe('renderEmail (public)', () => {
  it('renders a complex tree with different content', () => {
    const Comp = () => <html><body><h3>Greetings</h3><p>Test paragraph</p></body></html>;
    const output = renderEmail(<Comp />);
    expect(output.startsWith('<!DOCTYPE html')).toBe(true);
    expect(output).toContain('<h3>Greetings</h3>');
    expect(output).toContain('Test paragraph');
  });

  it('renders a bare section element', () => {
    const output = renderEmail(<section />);
    expect(output).toContain('<section');
  });
});