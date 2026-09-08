// Tests for ConfigRunner main logic and error paths
const { expect } = require('chai');
const Q = require('q');
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('ConfigRunner', function() {
  let logger, logSpy, GlobRunner, RemoteRunner, SyncedFileCollection, S3PromiseWrapper, AWS, fileUtils;
  beforeEach(() => {
    logSpy = [];
    logger = (...args) => logSpy.push(args.join(' '));
    GlobRunner = function(c) { this.addPattern = sinon.spy(); this.run = sinon.spy(); };
    RemoteRunner = function(b, c, s3w) { this.run = sinon.spy(); };
    class DummySyncedFile {
      constructor(p) { }
      static called = [];
    }
    fileUtils = { 
      getContents: sinon.stub().callsFake((p) => Q.resolve('filecontent'))
    };
    S3PromiseWrapper = function(s3) {
      this.putObject = sinon.stub().callsFake(() => Q.resolve());
      this.deleteObjects = sinon.stub().callsFake(() => Q.resolve());
    };
    AWS = {
      S3: function() { },
      config: { loadFromPath: sinon.spy() }
    };
    SyncedFileCollection = function() {
      this.allDone = Q.resolve([
        { action: 'upload', path: 'a.txt' },
        { action: 'delete', path: 'b.txt' }
      ]);
    };
  });

  it('should run ConfigRunner: credentials, upload, delete', async () => {
    const ConfigRunner = proxyquire('../src/ConfigRunner', {
      './GlobRunner': GlobRunner,
      './RemoteRunner': RemoteRunner,
      './SyncedFileCollection': SyncedFileCollection,
      './S3PromiseWrapper': S3PromiseWrapper,
      'aws-sdk': AWS,
      './file-utils': fileUtils
    }).TestHook(GlobRunner, RemoteRunner, SyncedFileCollection, S3PromiseWrapper, AWS, fileUtils);

    // Stub console.log to capture uploads and deletes
    const origLog = console.log;
    const out = [];
    console.log = (...args) => out.push(args.join(' '));
    const config = {
      credentials: 'creds.json',
      bucketName: 'bucket',
      patterns: ['*.js', '*.txt']
    };
    const runner = new ConfigRunner();
    runner.setConfig(config).run();
    // Wait for allDone etc to drain
    await Q.delay(30);

    expect(out.join('\n')).to.include('uploading: a.txt');
    expect(out.join('\n')).to.include('deleting');
    expect(AWS.config.loadFromPath.calledOnce).to.be.true;
    console.log = origLog;
  });

  it('should handle no credentials', async () => {
    const ConfigRunner = proxyquire('../src/ConfigRunner', {
      './GlobRunner': GlobRunner,
      './RemoteRunner': RemoteRunner,
      './SyncedFileCollection': SyncedFileCollection,
      './S3PromiseWrapper': S3PromiseWrapper,
      'aws-sdk': AWS,
      './file-utils': fileUtils
    }).TestHook(GlobRunner, RemoteRunner, SyncedFileCollection, S3PromiseWrapper, AWS, fileUtils);

    let logHits = [];
    const origLog = console.log;
    console.log = (...args) => logHits.push(args.join(' '));
    const config = {
      bucketName: 'bucket',
      patterns: ['*.js']
    };
    const runner = new ConfigRunner();
    runner.setConfig(config).run();
    await Q.delay(15);

    expect(logHits.join('\n')).to.not.include('error');
    expect(AWS.config.loadFromPath.called).to.be.false;
    console.log = origLog;
  });

  it('should call forAll patterns', () => {
    // Test that all patterns are passed to globRunner.addPattern
    let handled = [];
    GlobRunner = function() {
      this.addPattern = (p) => handled.push(p);
      this.run = sinon.spy();
    };
    SyncedFileCollection = function() { this.allDone = Q(Q.resolve([])); };
    const ConfigRunner = proxyquire('../src/ConfigRunner', {
      './GlobRunner': GlobRunner,
      './RemoteRunner': RemoteRunner,
      './SyncedFileCollection': SyncedFileCollection,
      './S3PromiseWrapper': S3PromiseWrapper,
      'aws-sdk': AWS,
      './file-utils': fileUtils
    }).TestHook(GlobRunner, RemoteRunner, SyncedFileCollection, S3PromiseWrapper, AWS, fileUtils);

    const config = {
      bucketName: 'bucket',
      patterns: ['*.foo', '*.bar']
    };
    const runner = new ConfigRunner();
    runner.setConfig(config).run();
    expect(handled).to.eql(['*.foo', '*.bar']);
  });
});