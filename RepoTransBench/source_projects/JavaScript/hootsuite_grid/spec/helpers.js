// helpers.js for spec utility functions

function addIndexesToItems(items) {
    items.forEach(function(item, idx) {
        item.i = idx;
    });
}
exports.addIndexesToItems = addIndexesToItems;

// Add other helper stubs here as needed for running specs