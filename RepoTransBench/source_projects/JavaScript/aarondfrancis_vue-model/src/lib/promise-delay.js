// This file didn't support "require". Let's patch it so it's usable for testing.
function delay(ms, value) {
  return new Promise(resolve => setTimeout(() => resolve(value), ms));
}

module.exports = delay;