const config = require('../config');

describe('config.js', () => {
  const OLD_ENV = process.env;
  beforeEach(() => {
    jest.resetModules();
    process.env = { ...OLD_ENV };
  });
  afterAll(() => {
    process.env = OLD_ENV;
  });

  it('should export kmsEncryptedHookUrl from env', () => {
    process.env.KMS_ENCRYPTED_HOOK_URL = 'encryptedurl';
    delete require.cache[require.resolve('../config')];
    const cfg = require('../config');
    expect(cfg.kmsEncryptedHookUrl).toBe('encryptedurl');
  });

  it('should export unencryptedHookUrl from env', () => {
    process.env.UNENCRYPTED_HOOK_URL = 'unencryptedurl';
    delete require.cache[require.resolve('../config')];
    const cfg = require('../config');
    expect(cfg.unencryptedHookUrl).toBe('unencryptedurl');
  });

  it('should contain services with correct match_text', () => {
    expect(config.services.elasticbeanstalk.match_text).toBe('ElasticBeanstalkNotifications');
    expect(config.services.codedeploy.match_text).toBe('CodeDeploy');
    expect(config.services.codepipeline.match_text).toBe('CodePipelineNotifications');
    expect(config.services.elasticache.match_text).toBe('ElastiCache');
    expect(config.services.autoscaling.match_text).toBe('AutoScaling');
    expect(typeof config.services.cloudwatch).toBe('object');
  });
});