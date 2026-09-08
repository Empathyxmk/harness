/*global process*/
const Buffer = require('safe-buffer').Buffer;
const fs = require('fs');
const test = require('tape');
const jws = require('..');

const NODE_VERSION = require('semver').clean(process.version);
const SUPPORTS_ENCRYPTED_KEYS = require('semver').gte(NODE_VERSION, '0.11.8');

function readfile(path) {
  return fs.readFileSync(__dirname.replace('test_public', 'test') + '/' + path).toString();
}

function readstream(path) {
  return fs.createReadStream(__dirname.replace('test_public', 'test') + '/' + path);
}

const rsaPrivateKey = readfile('rsa-private.pem');
const rsaPrivateKeyEncrypted = readfile('rsa-private-encrypted.pem');
const encryptedPassphrase = readfile('encrypted-key-passphrase');
const rsaPublicKey = readfile('rsa-public.pem');
const rsaWrongPublicKey = readfile('rsa-wrong-public.pem');
const ecdsaPrivateKey = {
  '256': readfile('ec256-private.pem'),
  '384': readfile('ec384-private.pem'),
  '512': readfile('ec512-private.pem'),
};
const ecdsaPublicKey = {
  '256': readfile('ec256-public.pem'),
  '384': readfile('ec384-public.pem'),
  '512': readfile('ec512-public.pem'),
};
const ecdsaWrongPublicKey = {
  '256': readfile('ec256-wrong-public.pem'),
  '384': readfile('ec384-wrong-public.pem'),
  '512': readfile('ec512-wrong-public.pem'),
};

const BITS = ['256', '384', '512'];
const CURVES = {
  '256': '256',
  '384': '384',
  '512': '521',
};

const publicPayloadString = 'hola мир 李小龙 : @©®†¥πç√∫˜µ≤≥÷';
const publicPayload = {
  title: publicPayloadString,
  items: ['alpha', 8, 5]
};

BITS.forEach(function (bits) {
  test('HMAC using SHA-'+bits+' hash algorithm (public)', function (t) {
    const alg = 'HS'+bits;
    const header = { alg: alg, typ: 'JWT' };
    const secret = 'notsosecret';
    const jwsObj = jws.sign({
      header: header,
      payload: publicPayload,
      secret: secret,
      encoding: 'utf8',
    });
    const parts = jws.decode(jwsObj);
    t.ok(jws.verify(jwsObj, alg, secret), 'should verify');
    t.notOk(jws.verify(jwsObj, alg, 'badsecret'), 'should not verify with non-matching secret');
    t.same(parts.payload, publicPayload, 'should match payload');
    t.same(parts.header, header, 'should match header');
    t.end();
  });
});

BITS.forEach(function (bits) {
  test('RSASSA using SHA-'+bits+' hash algorithm (public)', function (t) {
    const alg = 'RS'+bits;
    const header = { alg: alg };
    const privateKey = rsaPrivateKey;
    const publicKey = rsaPublicKey;
    const wrongPublicKey = rsaWrongPublicKey;
    const jwsObj = jws.sign({
      header: header,
      payload: publicPayload,
      privateKey: privateKey
    });
    const parts = jws.decode(jwsObj, { json: true });
    t.ok(jws.verify(jwsObj, alg, publicKey), 'should verify');
    t.notOk(jws.verify(jwsObj, alg, wrongPublicKey), 'should not verify with non-matching public key');
    t.notOk(jws.verify(jwsObj, 'HS'+bits, publicKey), 'should not verify with non-matching algorithm');
    t.same(parts.payload, publicPayload, 'should match payload');
    t.same(parts.header, header, 'should match header');
    t.end();
  });
});

BITS.forEach(function (bits) {
  const curve = CURVES[bits];
  test('ECDSA using P-'+curve+' curve and SHA-'+bits+' hash algorithm (public)', function (t) {
    const alg = 'ES'+bits;
    const header = { alg: alg };
    const privateKey = ecdsaPrivateKey[bits];
    const publicKey = ecdsaPublicKey[bits];
    const wrongPublicKey = ecdsaWrongPublicKey[bits];
    const jwsObj = jws.sign({
      header: header,
      payload: publicPayloadString,
      privateKey: privateKey
    });
    const parts = jws.decode(jwsObj);
    t.ok(jws.verify(jwsObj, alg, publicKey), 'should verify');
    t.notOk(jws.verify(jwsObj, alg, wrongPublicKey), 'should not verify with non-matching public key');
    t.notOk(jws.verify(jwsObj, 'HS'+bits, publicKey), 'should not verify with non-matching algorithm');
    t.same(parts.payload, publicPayloadString, 'should match payload');
    t.same(parts.header, header, 'should match header');
    t.end();
  });
});

test('No digital signature or MAC value included (public)', function (t) {
  const alg = 'none';
  const header = { alg: alg };
  const payload = '¡Hola Mundo!';
  const jwsObj = jws.sign({
    header: header,
    payload: payload,
  });
  const parts = jws.decode(jwsObj);
  t.ok(jws.verify(jwsObj, alg), 'should verify');
  t.ok(jws.verify(jwsObj, alg, 'really anything'), 'should still verify');
  t.notOk(jws.verify(jwsObj, 'HS256', 'anything'), 'should not verify with non-matching algorithm');
  t.same(parts.payload, payload, 'should match payload');
  t.same(parts.header, header, 'should match header');
  t.end();
});

test('Streaming sign: HMAC (public)', function (t) {
  const dataStream = readstream('data.txt');
  const secret = 'supersecret';
  const sig = jws.createSign({
    header: { alg: 'HS384' },
    secret: secret
  });
  dataStream.pipe(sig.payload);
  sig.on('done', function (signature) {
    t.ok(jws.verify(signature, 'HS384', secret), 'should verify');
    t.end();
  });
});

test('Streaming sign: RSA (public)', function (t) {
  const dataStream = readstream('data.txt');
  const privateKeyStream = readstream('rsa-private.pem');
  const publicKey = rsaPublicKey;
  const wrongPublicKey = rsaWrongPublicKey;
  const sig = jws.createSign({
    header: { alg: 'RS384' },
  });
  dataStream.pipe(sig.payload);

  process.nextTick(function () {
    privateKeyStream.pipe(sig.key);
  });

  sig.on('done', function (signature) {
    t.ok(jws.verify(signature, 'RS384', publicKey), 'should verify');
    t.notOk(jws.verify(signature, 'RS384', wrongPublicKey), 'should not verify');
    t.same(jws.decode(signature).payload, fs.readFileSync(__dirname.replace('test_public', 'test') + '/data.txt').toString(), 'payload should match file content');
    t.end();
  });
});