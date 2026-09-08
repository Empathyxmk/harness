// Load modules.
var OAuthStrategy, OAuth2Strategy;
try {
  OAuthStrategy = require('passport-google-oauth1');
} catch (e) {
  throw new Error('passport-google-oauth1 must be installed');
}
try {
  OAuth2Strategy = require('passport-google-oauth20');
} catch (e) {
  throw new Error('passport-google-oauth20 must be installed');
}

// Exports.
exports.Strategy =
exports.OAuthStrategy = OAuthStrategy;
exports.OAuth2Strategy = OAuth2Strategy;