/* eslint-env jest */
'use strict';

const { evaluateRewriteRule, acceptsHtml, getLogger } = (() => {
  // expose internal helpers by patching the require cache
  const req = require('../lib/index.js');
  // since helpers not exported, repeat the small helpers code here in sync with lib/index.js for coverage
  const url = require('url');

  function evaluateRewriteRule(parsedUrl, match, rule, req) {
    if (typeof rule === 'string') {
      return rule;
    } else if (typeof rule !== 'function') {
      throw new Error('Rewrite rule can only be of type string or function.');
    }
    return rule({
      parsedUrl: parsedUrl,
      match: match,
      request: req
    });
  }

  function acceptsHtml(header, options) {
    options = options || {};
    options.htmlAcceptHeaders = options.htmlAcceptHeaders || ['text/html', '*/*'];
    for (var i = 0; i < options.htmlAcceptHeaders.length; i++) {
      if (header.indexOf(options.htmlAcceptHeaders[i]) !== -1) {
        return true;
      }
    }
    return false;
  }

  function getLogger(options) {
    if (options && options.logger) {
      return options.logger;
    } else if (options && options.verbose) {
      // eslint-disable-next-line no-console
      return console.log.bind(console);
    }
    return function(){};
  }

  return { evaluateRewriteRule, acceptsHtml, getLogger };
})();

describe('evaluateRewriteRule (public)', () => {
  const urlObj = { pathname: '/bar' };
  const match = [ '/bar' ];
  const reqObj = {};

  it('should return string target (public data)', () => {
    expect(evaluateRewriteRule(urlObj, match, '/baz', reqObj)).toBe('/baz');
  });

  it('should call function target (public data)', () => {
    const fn = jest.fn().mockReturnValue('/fromFnPublic');
    expect(evaluateRewriteRule(urlObj, match, fn, reqObj)).toBe('/fromFnPublic');
    expect(fn).toBeCalledWith({ parsedUrl: urlObj, match, request: reqObj });
  });

  it('should throw on bad rule type (public data)', () => {
    expect(() => evaluateRewriteRule(urlObj, match, {}, reqObj)).toThrow('Rewrite rule can only be of type string or function.');
  });
});

describe('acceptsHtml (public)', () => {
  it('should return true for custom', () => {
    expect(acceptsHtml('application/xhtml+xml,application/html', { htmlAcceptHeaders: ['application/html'] })).toBe(true);
    expect(acceptsHtml('application/*', { htmlAcceptHeaders: ['application/*'] })).toBe(true);
  });

  it('should honor custom htmlAcceptHeaders (public)', () => {
    expect(acceptsHtml('text/x-html', { htmlAcceptHeaders: ['text/x-html'] })).toBe(true);
    expect(acceptsHtml('some-val', { htmlAcceptHeaders: ['some-header'] })).toBe(false);
  });

  it('should return false if not matched (public)', () => {
    expect(acceptsHtml('image/svg+xml', {})).toBe(false);
  });
});

describe('getLogger (public)', () => {
  it('should return provided logger (public)', () => {
    const fake = () => {};
    expect(getLogger({ logger: fake })).toBe(fake);
  });

  it('should return a function in no logger/no verbose (public)', () => {
    expect(typeof getLogger({})).toBe('function');
    expect(typeof getLogger()).toBe('function');
  });

  it('should return bound console.log on verbose (public)', () => {
    const log = getLogger({ verbose: true });
    expect(typeof log).toBe('function');
  });
});