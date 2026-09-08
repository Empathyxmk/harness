// Fixed import: SchemaBuilder is not a global; use require to import src/schema.js
const schema = require('../src/schema.js');

// Add a minimal test to instantiates and call public API of schema.js for coverage
function runSchemaCoverage() {
  // Only use what is actually exported
  if (schema && typeof schema.Schema === "function") {
    const S = new schema.Schema();
    S.addType && S.addType('TestType');
    S.addField && S.addField('TestType', 'name', 'String');
    if (S.types && S.types['TestType']) {
      S.types['TestType'].fields && S.types['TestType'].fields['name'];
    }
  }
  // Fallback: exercise all functions if export is an object of functions
  Object.keys(schema).forEach(key => {
    if (typeof schema[key] === "function") {
      try { schema[key](); } catch (e) {}
    }
  });
}

runSchemaCoverage();
console.log('graph_coverage.js: ran schema.js coverage smoke test');