// Use only standard JS, not Vue.set, to avoid dependency issues
function setNested(obj, path, value, separator = '.') {
  const keys = path.split(separator);
  let o = obj;
  while (keys.length > 1) {
    const k = keys.shift();
    if (typeof o[k] !== 'object' || o[k] === null) o[k] = {};
    o = o[k];
  }
  o[keys[0]] = value;
  return obj;
}

module.exports = setNested;