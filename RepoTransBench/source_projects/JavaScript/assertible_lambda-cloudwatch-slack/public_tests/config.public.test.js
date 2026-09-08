const config = require('../config');

describe('config.js (public test data)', () => {
  const OLD_ENV = process.env;
  beforeEach(() => {
    jest.resetModules();
    process.env = { ...OLD_ENV };
  });
  afterAll(() => {
    process.env = OLD_ENV;
  });

  it('exports a different kmsEncryptedHookUrl from env', () => {
    process.env.KMS_ENCRYPTED_HOOK_URL = 'public_encrypted_url_xyz';
    delete require.cache[require.resolve('../config')];
    const cfg = require('../config');
    expect(cfg.kmsEncryptedHookUrl).toBe('public_encrypted_url_xyz');
  });

  it('exports a different unencryptedHookUrl from env', () => {
    process.env.UNENCRYPTED_HOOK_URL = 'public_unencrypted_url_abc';
    delete require.cache[require.resolve('../config')];
    const cfg = require('../config');
    expect(cfg.unencryptedHookUrl).toBe('public_unencrypted_url_abc');
  });

  it('contains expected service keys and public match_text', () => {
    expect(config.services.elasticbeanstalk.match_text).toContain('ElasticBeanstalk');
    expect(config.services.codedeploy.match_text).toBe('CodeDeploy');
    expect(Object.keys(config.services)).toEqual(
      expect.arrayContaining(['cloudwatch', 'autoscaling', 'elasticbeanstalk', 'codepipeline', 'codedeploy', 'elasticache'])
    );
    expect(typeof config.services.cloudwatch).toBe('object');
  });
});