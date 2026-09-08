// @benface/tailwindcss-transforms plugin main module

function prefixNegativeModifiers(object = {}) {
  let newObject = {};
  Object.keys(object).forEach(key => {
    let value = object[key];
    if (typeof value === 'string') {
      newObject[key] = value;
    } else if (typeof value === 'number' && value < 0) {
      newObject[key] = `${value}`;
    } else if (typeof value === 'number') {
      newObject[key] = `${value}`;
    } else {
      newObject[key] = value;
    }
  });
  return newObject;
}

function transformsPlugin({ addUtilities, addComponents, theme, variants, e }, pluginOptions = {}) {
  // Utility definitions (very simplified for testability)
  const translate = theme('translate') || {};
  const scale = theme('scale') || {};
  const rotate = theme('rotate') || {};
  const skew = theme('skew') || {};
  const transformOrigin = theme('transformOrigin') || {};

  const utilities = {
    '.transform-none': { transform: 'none' },
    ...Object.entries(translate).reduce((acc, [key, val]) => {
      acc[`.translate-x-${key}`] = { transform: `translateX(${val})` };
      acc[`.translate-y-${key}`] = { transform: `translateY(${val})` };
      return acc;
    }, {})
  };

  addUtilities(utilities, variants && variants('transform'));

  const components = {
    '.transform-center': { 'transform-origin': 'center' },
    ...Object.entries(transformOrigin).reduce((acc, [key, val]) => {
      acc[`.transform-${key}`] = { 'transform-origin': val };
      return acc;
    }, {})
  };
  addComponents(components);
}

module.exports = transformsPlugin;
module.exports.prefixNegativeModifiers = prefixNegativeModifiers;