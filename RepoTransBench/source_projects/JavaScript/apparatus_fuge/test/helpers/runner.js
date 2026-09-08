// Patch: fix how fuge is imported, handle both function and object export
let fugeMod = require('../../fuge.js');
// fuge.js now exports a function, so just assign directly and skip call
module.exports = fugeMod;