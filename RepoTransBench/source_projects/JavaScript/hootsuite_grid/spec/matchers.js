// matchers.js for custom Jasmine matchers (Jasmine v3+ API)
beforeAll(function() {
  jasmine.addMatchers({
    toBeLike: function() {
      return {
        compare: function(actual, expected) {
          var result = {};
          result.pass = JSON.stringify(actual) === JSON.stringify(expected);
          if (result.pass) {
            result.message = 'Passed';
          } else {
            result.message = "Expected " + JSON.stringify(actual) + " to equal " + JSON.stringify(expected);
          }
          return result;
        }
      };
    }
  });
});