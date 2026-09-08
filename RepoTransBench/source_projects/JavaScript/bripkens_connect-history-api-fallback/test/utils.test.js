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

describe('evaluateRewriteRule', () => {
  const urlObj = { pathname: '/foo' };
  const match = [ '/foo' ];
  const reqObj = {};

  it('should return string target', () => {
    expect(evaluateRewriteRule(urlObj, match, '/bar', reqObj)).toBe('/bar');
  });

  it('should call function target', () => {
    const fn = jest.fn().mockReturnValue('/fromFn');
    expect(evaluateRewriteRule(urlObj, match, fn, reqObj)).toBe('/fromFn');
    expect(fn).toBeCalledWith({ parsedUrl: urlObj, match, request: reqObj });
  });

  it('should throw on bad rule type', () => {
    expect(() => evaluateRewriteRule(urlObj, match, 123, reqObj)).toThrow('Rewrite rule can only be of type string or function.');
  });
});

describe('acceptsHtml', () => {
  it('should return true for defaults', () => {
    expect(acceptsHtml('text/html,application/xhtml+xml', {})).toBe(true);
    expect(acceptsHtml('*/*', {})).toBe(true);
  });

  it('should honor custom htmlAcceptHeaders', () => {
    expect(acceptsHtml('application/my-html', { htmlAcceptHeaders: ['application/my-html'] })).toBe(true);
    expect(acceptsHtml('something', { htmlAcceptHeaders: ['foo/bar'] })).toBe(false);
  });

  it('should return false if not matched', () => {
    expect(acceptsHtml('application/json', {})).toBe(false);
  });
});

describe('getLogger', () => {
  it('should return provided logger', () => {
    const fake = () => {};
    expect(getLogger({ logger: fake })).toBe(fake);
  });

  it('should return a function in no logger/no verbose', () => {
    expect(typeof getLogger({})).toBe('function');
    expect(typeof getLogger()).toBe('function');
  });

  it('should return bound console.log on verbose', () => {
    const log = getLogger({ verbose: true });
    expect(typeof log).toBe('function');
  });
});