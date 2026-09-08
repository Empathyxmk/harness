// Utility functions for array operations

exports.length = function(arr) {
  if (!Array.isArray(arr)) return 0;
  return arr.length;
};

exports.min = function(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  if (arr.every(el => el === null)) return null;
  var filtered = arr.filter(el => el !== null && el !== undefined);
  if (filtered.length === 0) return undefined;
  // If filtered includes objects with {"__null__":true}, treat that as null
  if (filtered.length === 1 && filtered[0] && filtered[0].__null__ === true) return null;
  return Math.min.apply(null, filtered);
};

exports.max = function(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  if (arr.every(el => el === null)) return null;
  var filtered = arr.filter(el => el !== null && el !== undefined);
  if (filtered.length === 0) return undefined;
  if (filtered.length === 1 && filtered[0] && filtered[0].__null__ === true) return null;
  return Math.max.apply(null, filtered);
};

exports.sum = function(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  if (arr.every(el => el === null)) return null;
  var filtered = arr.filter(el => el !== null && el !== undefined);
  if (filtered.length === 0) return undefined;
  if (filtered.length === 1 && filtered[0] && filtered[0].__null__ === true) return null;
  return filtered.reduce(function(prev, curr) {
    return Number(prev) + Number(curr);
  }, 0);
};

exports.avg = function(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  if (arr.every(el => el === null)) return null;
  var filtered = arr.filter(el => el !== null && el !== undefined);
  if (filtered.length === 0) return undefined;
  if (filtered.length === 1 && filtered[0] && filtered[0].__null__ === true) return null;
  return exports.sum(filtered) / filtered.length;
};

exports.concat = function(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return undefined;
  if (arr.every(el => el === null)) return null;
  var filtered = arr.filter(el => el !== null && el !== undefined);
  if (filtered.length === 0) return undefined;
  if (filtered.some(el => el && el.__null__ === true)) {
    // If any element is {__null__:true}, treat as 'null' string
    return arr.map(el => (el && el.__null__ === true) ? 'null' : String(el)).join('');
  }
  return filtered.map(String).join('');
};