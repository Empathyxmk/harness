// src/Squire.node.js
// Node-friendly export for Squire utilities to make unit testing feasible
// This is a "bridge" file for Jest-style unit testing, since src/Squire.js is wrapped as a RequireJS AMD module.

const SquireCore = (() => {
  // Copy/paste/convert the main Squire utility functions from src/Squire.js

  const toString = Object.prototype.toString;

  function isArray(arr) {
    return toString.call(arr) === '[object Array]';
  }

  function isFunction(fn) {
    return toString.call(fn) === '[object Function]';
  }

  function indexOf(arr, search) {
    for (let i = 0, length = arr.length; i < length; i++) {
      if (arr[i] === search) {
        return i;
      }
    }
    return -1;
  }

  function each(obj, iterator, context) {
    const breaker = {};
    if (obj === null) {
      return;
    }
    if (Array.prototype.forEach && obj.forEach === Array.prototype.forEach) {
      obj.forEach(iterator, context);
    } else if (obj.length === +obj.length) {
      for (let i = 0, l = obj.length; i < l; i++) {
        if (iterator.call(context, obj[i], i, obj) === breaker) {
          return;
        }
      }
    } else {
      for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
          if (iterator.call(context, obj[key], key, obj) === breaker) {
            return;
          }
        }
      }
    }
  }

  function extend(obj) {
    each(Array.prototype.slice.call(arguments, 1), function (source) {
      if (source) {
        for (const prop in source) {
          if (Object.prototype.hasOwnProperty.call(source, prop)) {
            obj[prop] = source[prop];
          }
        }
      }
    });
    return obj;
  }

  function clone(obj) {
    if (!obj || typeof obj !== 'object') return obj;
    if (isArray(obj)) return obj.slice();
    return extend({}, obj);
  }

  // Export all utilities for test/require
  return {
    isArray,
    isFunction,
    indexOf,
    each,
    extend,
    clone,
  };
})();

module.exports = SquireCore;