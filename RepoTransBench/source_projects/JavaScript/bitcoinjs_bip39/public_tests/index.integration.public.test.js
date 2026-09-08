const assert = require('assert');
const bip39 = require('../index.js');

// Public test mnemonics/entropy/PASSWORD should be different than the existing suite
const VALID_MNEMONIC = "legal winner thank year wave sausage worth useful legal winner thank yellow";
const INVALID_MNEMONIC = "hello world example lorem ipsum dolor sit amet consectetuer adipiscing elit";
const VALID_ENTROPY = "2e8905819b8723fe2c1d161860e5ee1830318dbf49a83bd451cfb8440c28bd6f";
const INVALID_ENTROPY = "xyz_not_a_hex_1234";
const PASSWORD = "OpenAI123!";

describe('bip39 main integration (public)', function() {
  it('generates mnemonic from entropy (public)', function() {
    // Using new entropy (longer string)
    const mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY);
    assert.strictEqual(typeof mnemonic, 'string');
    assert.strictEqual(mnemonic.split(' ').length, 24);
  });

  it('generates entropy from mnemonic (public)', function() {
    // This VALID_MNEMONIC corresponds to VALID_ENTROPY from the real bip39 vectors
    const entropy = bip39.mnemonicToEntropy(VALID_MNEMONIC);
    assert.strictEqual(typeof entropy, 'string');
    assert.strictEqual(entropy, VALID_ENTROPY);
  });

  it('validates correct mnemonic (public)', function() {
    assert.strictEqual(bip39.validateMnemonic(VALID_MNEMONIC), true);
  });

  it('invalidates incorrect mnemonic (public)', function() {
    assert.strictEqual(bip39.validateMnemonic(INVALID_MNEMONIC), false);
  });

  it('throws on entropyToMnemonic for invalid entropy (public)', function() {
    assert.throws(() => bip39.entropyToMnemonic(INVALID_ENTROPY), Error);
  });

  it('throws on mnemonicToEntropy for invalid mnemonic (public)', function() {
    assert.throws(() => bip39.mnemonicToEntropy(INVALID_MNEMONIC), Error);
  });

  it('can generateRandom mnemonic (public)', function() {
    const mnemonic = bip39.generateMnemonic();
    assert.strictEqual(typeof mnemonic, 'string');
    assert(mnemonic.split(' ').length === 12 || mnemonic.split(' ').length === 24);
    assert.strictEqual(bip39.validateMnemonic(mnemonic), true);
  });

  it('generates and validates seed from mnemonic (public)', function(done) {
    this.timeout(5000);
    bip39.mnemonicToSeed(VALID_MNEMONIC, PASSWORD)
      .then(seed => {
        assert(seed instanceof Buffer || Buffer.isBuffer(seed));
        assert.strictEqual(seed.length, 64);
        done();
      })
      .catch(done);
  });

  it('generates and validates seedSync from mnemonic (public)', function() {
    const seed = bip39.mnemonicToSeedSync(VALID_MNEMONIC, PASSWORD);
    assert(seed instanceof Buffer || Buffer.isBuffer(seed));
    assert.strictEqual(seed.length, 64);
  });

  it('supports custom wordlists (public)', function() {
    // Use a non-english wordlist (e.g., French) to generate mnemonic/entropy
    const french = bip39.wordlists && bip39.wordlists.french;
    assert(Array.isArray(french), 'french wordlist present');
    assert.strictEqual(french.length, 2048);
    const mnemonic = bip39.entropyToMnemonic(VALID_ENTROPY, french);
    assert.strictEqual(typeof mnemonic, 'string');
    assert.strictEqual(mnemonic.split(' ').length, 24);
  });
});