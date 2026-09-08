// Public extra test for src/ConfigRunner.js using different config patterns
const { expect } = require('chai');
const proxyquire = require('proxyquire');

describe('ConfigRunner (public data)', function() {
  let ConfigRunner, called;
  beforeEach(() => {
    called = {
      runGlob: false,
      runRemote: false,
      getContents: []
    };

    const GlobRunner = function(collection) {
      this.patterns = [];
      this.addPattern = (pat) => this.patterns.push(pat);
      this.run = () => { called.runGlob = true; };
    };
    const RemoteRunner = function(bucket, collection, s3Wrapper) {
      this.run = () => { called.runRemote = true; };
    };
    const SyncedFileCollection = function() {
      this.allDone = Promise.resolve([
        { action: 'upload', path: 'img2.jpg' },
        { action: 'delete', path: 'old2.txt' }
      ]);
      this.foundFile = () => {};
      this.foundRemote = () => {};
    };
    const S3PromiseWrapper = function(s3) {
      this.putObject = (bucket, path, contents) => {
        called.getContents.push(path);
        return Promise.resolve();
      };
      this.deleteObjects = (bucket, deletes) => { called.deleted = deletes; return Promise.resolve(); };
    };
    const AWS = { S3: function() {}, config: { loadFromPath: () => { called.cred = true; } } };
    const fileUtils = {
      getContents: async (path) => ({ path }),
    };

    ConfigRunner = proxyquire('../src/ConfigRunner', {})
      .TestHook(GlobRunner, RemoteRunner, SyncedFileCollection, S3PromiseWrapper, AWS, fileUtils);
  });

  it('should call run on public fake runners and perform correct actions', async () => {
    const runner = new ConfigRunner();
    const conf = {
      credentials: 'public/creds.json',
      bucketName: 'public_bucket2',
      patterns: [ 'img2.jpg', 'old2.txt' ]
    };
    runner.setConfig(conf);
    runner.run();
    await new Promise(r => setTimeout(r, 10));
    expect(called.runGlob).to.be.true;
    expect(called.runRemote).to.be.true;
    expect(called.cred).to.be.true;
    expect(called.getContents).to.contain('img2.jpg');
    expect(called.deleted).to.include('old2.txt');
  });
});