const postcss = require("postcss");

module.exports = postcss.plugin("postcss-icss-selectors", () => {
  return (root) => {
    let icssSelectors = [];
    root.walkRules((rule) => {
      if (rule.selector === ":icss-selector") {
        rule.walkDecls("-icss-selector", (decl) => {
          icssSelectors.push(decl.value);
        });
        rule.remove();
      }
    });
    if (icssSelectors.length) {
      let selector = icssSelectors[icssSelectors.length - 1];
      root.walkRules((rule) => {
        // Only rewrite selectors for rules that start with a class or id
        if (rule.selector !== ":icss-selector") {
          rule.selector = rule.selector.replace(/^([#.]?)[^\s>+~]*/, selector);
        }
      });
    }
  };
});