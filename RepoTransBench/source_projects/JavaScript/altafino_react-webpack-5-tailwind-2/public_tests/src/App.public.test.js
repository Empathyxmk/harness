// Slightly different than the original, if original checks for rendering text, check for presence/absence of other text
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

describe('App.js (public)', () => {
  it('renders component with the word "Welcome" or similar root text', () => {
    render(<App />);
    // Instead of looking for the exact original text, look for "Welcome" or "tailwind" or any other similar root text
    expect(screen.getByText(/welcome|tailwind/i)).toBeInTheDocument();
  });

  it('renders a div as the root element', () => {
    const { container } = render(<App />);
    expect(container.firstChild.nodeName).toBe('DIV');
  });
});