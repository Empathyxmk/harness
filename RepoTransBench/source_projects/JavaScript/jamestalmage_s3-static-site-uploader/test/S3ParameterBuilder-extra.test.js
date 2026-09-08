// Extra tests for S3ParameterBuilder
const { expect } = require('chai');
const S3ParameterBuilder = require('../src/S3ParameterBuilder');

describe('S3ParameterBuilder', () => {
  it('should create params for createBucket', () => {
    expect(S3ParameterBuilder.createBucket('foo')).to.eql({ Bucket:'foo' });
  });

  it('should create headBucket params', () => {
    expect(S3ParameterBuilder.headBucket('mine')).to.eql({ Bucket:'mine' });
  });

  it('should create putBucketPolicy params', () => {
    const pol = { x: 1 };
    const out = S3ParameterBuilder.putBucketPolicy('b', pol);
    expect(out.Bucket).to.equal('b');
    expect(JSON.parse(out.Policy)).to.eql(pol);
  });

  it('should create putObject params with/without mimeType', () => {
    const result1 = S3ParameterBuilder.putObject('bucket', 'test.html', 'abc');
    expect(result1.Bucket).to.equal('bucket');
    expect(result1.Key).to.equal('test.html');
    expect(result1.Body).to.equal('abc');
    expect(result1).to.have.property('ContentType');
    const result2 = S3ParameterBuilder.putObject('bucket','f.txt','x','cust/type');
    expect(result2.ContentType).to.equal('cust/type');
  });

  it('should create putBucketWebsite params w/ index and error', () => {
    const r = S3ParameterBuilder.putBucketWebsite('b','index.html','err.html');
    expect(r.Bucket).to.equal('b');
    expect(r.WebsiteConfiguration.IndexDocument.Suffix).to.equal('index.html');
    expect(r.WebsiteConfiguration.ErrorDocument.Key).to.equal('err.html');
  });

  it('should create putBucketWebsite params missing args', () => {
    const r = S3ParameterBuilder.putBucketWebsite('x');
    expect(r).to.have.nested.property('WebsiteConfiguration');
    expect(r.WebsiteConfiguration).to.eql({});
  });

  it('should create listObjects with prefix', () => {
    expect(S3ParameterBuilder.listObjects('foo','prefix'))
      .to.eql({ Bucket:'foo', Prefix:'prefix' });
  });
  it('should create listObjects without prefix', () => {
    expect(S3ParameterBuilder.listObjects('foo'))
      .to.eql({ Bucket:'foo' });
  });

  it('should create deleteObjects params', () => {
    const keys = ['a','b'];
    const res = S3ParameterBuilder.deleteObjects('myb', keys);
    expect(res.Bucket).to.equal('myb');
    expect(res.Delete.Objects).to.eql([{Key:'a'}, {Key:'b'}]);
  });
});