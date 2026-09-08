const assert = require('assert');
const bip39 = require('../index.js');

// Helper mnemonic and entropy samples
const VALID_MNEMONIC = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about";
const INVALID_MNEMONIC = "foo bar baz qux quux corge grault garply waldo fred plugh xyzzy";
const VALID_ENTROPY = "00000000000000000000000000000000";
const INVALID_ENTROPY = "not_hex_string";
const PASSWORD = "TREZOR";

describe('bip39 main integration', function() {
  it('generates mnemonic from entropy', function() {
    const mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY);
    assert.strictEqual(typeof mnemonic, 'string');
    assert.strictEqual(mnemonic.split(' ').length, 12);
  });

  it('generates entropy from mnemonic', function() {
    const entropy = bip39.mnemonicToEntropy(VALID_MNEMONIC);
    assert.strictEqual(entropy, VALID_ENTROPY);
  });

  it('validates correct mnemonic', function() {
    assert.strictEqual(bip39.validateMnemonic(VALID_MNEMONIC), true);
  });

  it('invalidates incorrect mnemonic', function() {
    assert.strictEqual(bip39.validateMnemonic(INVALID_MNEMONIC), false);
  });

  it('throws on entropyToMnemonic for invalid entropy', function() {
    assert.throws(() => bip39.entropyToMnemonic(INVALID_ENTROPY), Error);
  });

  it('throws on mnemonicToEntropy for invalid mnemonic', function() {
    assert.throws(() => bip39.mnemonicToEntropy(INVALID_MNEMONIC), Error);
  });

  it('can generateRandom mnemonic', function() {
    const mnemonic = bip39.generateMnemonic();
    assert.strictEqual(typeof mnemonic, 'string');
    assert(mnemonic.split(' ').length === 12 || mnemonic.split(' ').length === 24);
    assert.strictEqual(bip39.validateMnemonic(mnemonic), true);
  });

  it('generates and validates seed from mnemonic', function(done) {
    this.timeout(5000);
    bip39.mnemonicToSeed(VALID_MNEMONIC, PASSWORD)
      .then(seed => {
        assert(seed instanceof Buffer || Buffer.isBuffer(seed));
        assert.strictEqual(seed.length, 64);
        done();
      })
      .catch(done);
  });

  it('generates and validates seedSync from mnemonic', function() {
    const seed = bip39.mnemonicToSeedSync(VALID_MNEMONIC, PASSWORD);
    assert(seed instanceof Buffer || Buffer.isBuffer(seed));
    assert.strictEqual(seed.length, 64);
  });

  it('supports custom wordlists', function() {
    // Let's use the official wordlist obtained from the running code, not from test vectors.
    const english = bip39.wordlists && bip39.wordlists.english;
    assert(Array.isArray(english), 'english wordlist present');
    assert.strictEqual(english.length, 2048);
    const mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY, english);
    assert.strictEqual(typeof mnemonic, 'string');
    assert.strictEqual(mnemonic.split(' ').length, 12);
  });
});