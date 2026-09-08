const S3ParameterBuilder = require('../src/S3ParameterBuilder');
const assert = require('assert');

describe('S3ParameterBuilder coverage', function() {
  it('should create all bucket and object param types', function() {
    const builder = new S3ParameterBuilder({ bucket: 'foo', prefix: 'bar' });
    let params = builder.forCreateBucket();
    assert.strictEqual(params.Bucket, 'foo');

    params = builder.forHeadBucket();
    assert.strictEqual(params.Bucket, 'foo');

    params = builder.forPutBucketPolicy('policy');
    assert.strictEqual(params.Policy, 'policy');

    params = builder.forPutObject('file.txt', 'body!', 'mime/type', { CacheControl: 'max-age=60' });
    assert.strictEqual(params.ContentType, 'mime/type');
    params = builder.forPutObject('file.txt', 'body!', null, { });
    assert.strictEqual(params.hasOwnProperty('ContentType'), false);

    params = builder.forPutBucketWebsite('index.html', 'error.html');
    assert.strictEqual(params.WebsiteConfiguration.IndexDocument.Suffix, 'index.html');
    params = builder.forPutBucketWebsite(); // missing args branch
    assert(params.WebsiteConfiguration);

    params = builder.forListObjects('subdir/');
    assert.strictEqual(params.Prefix, 'subdir/');
    params = builder.forListObjects();
    assert(!params.Prefix);

    params = builder.forDeleteObjects(['x', 'y']);
    assert.deepStrictEqual(params.Delete.Objects, [ { Key: 'x' }, { Key: 'y' } ]);
  });
});