// Public extra test for src/S3ParameterBuilder.js with different config/data
const { expect } = require('chai');
const proxyquire = require('proxyquire');

describe('S3ParameterBuilder (public data)', function() {
  let S3ParameterBuilder;
  beforeEach(() => {
    S3ParameterBuilder = proxyquire('../src/S3ParameterBuilder', {});
  });

  it('should build params for different bucket/key', function() {
    const config = {
      bucket: 'public-bucket',
      key: 'files/image.png',
      acl: 'authenticated-read',
      cacheControl: 'no-store',
      contentType: 'image/png',
      meta: { uploadedBy: 'tester' }
    };
    const builder = new S3ParameterBuilder(config);
    const params = builder.build();
    expect(params.Bucket).to.equal('public-bucket');
    expect(params.Key).to.equal('files/image.png');
    expect(params.ACL).to.equal('authenticated-read');
    expect(params.CacheControl).to.equal('no-store');
    expect(params.ContentType).to.equal('image/png');
    expect(params.Metadata).to.deep.equal({ uploadedBy: 'tester' });
  });
});