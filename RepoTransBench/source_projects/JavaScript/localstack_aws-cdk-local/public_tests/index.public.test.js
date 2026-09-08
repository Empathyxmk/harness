const {
  isEnvTrue,
  EDGE_PORT,
  PROTOCOL,
  EnvironmentMisconfigurationError,
  configureEnvironment,
} = require('../src/index');

describe('isEnvTrue (public)', () => {
  it("should return true for environment variable set to 'true' (unique var)", () => {
    const env = { ABC_X: 'true' };
    expect(isEnvTrue(env, 'ABC_X')).toBe(true);
  });

  it("should return true for environment variable set to '1' (unique var)", () => {
    const env = { XYZ_Y: '1' };
    expect(isEnvTrue(env, 'XYZ_Y')).toBe(true);
  });

  it("should return false for environment variable set to '0'", () => {
    const env = { ZYX_XY: '0' };
    expect(isEnvTrue(env, 'ZYX_XY')).toBe(false);
  });

  it("should return false for unset environment variable (unique var)", () => {
    const env = {};
    expect(isEnvTrue(env, 'VAR_NOT_SET_PUBLIC')).toBe(false);
  });
});

describe('constants (public)', () => {
  it('EDGE_PORT uses default', () => {
    expect(EDGE_PORT).toBe(4566);
  });

  it('PROTOCOL should be http if USE_SSL is not set (public)', () => {
    expect(PROTOCOL).toBe('http');
  });
});

describe('EnvironmentMisconfigurationError (public)', () => {
  it('should hold message (different message)', () => {
    const err = new EnvironmentMisconfigurationError('public message 2');
    expect(err).toBeInstanceOf(Error);
    expect(err.message).toBe('public message 2');
  });
});

describe('configureEnvironment (public)', () => {
  it('should throw if AWS_ENDPOINT_URL set but AWS_ENDPOINT_URL_S3 not set', () => {
    const env = { AWS_ENDPOINT_URL: 'http://only-url.example.com' };
    expect(() => configureEnvironment(env, [])).toThrow(
      "If specifying 'AWS_ENDPOINT_URL' then 'AWS_ENDPOINT_URL_S3' must be specified"
    );
  });

  it('should not throw if both AWS_ENDPOINT_URL and AWS_ENDPOINT_URL_S3 set', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://unique-endpoint.test',
      AWS_ENDPOINT_URL_S3: 'http://unique-s3.test',
    };
    expect(() => configureEnvironment(env, [])).not.toThrow();
  });

  it('should allow allowlisted AWS_ vars (unique var name)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://end-url.com',
      AWS_ENDPOINT_URL_S3: 'http://s3-url.com',
      AWS_PUBLIC_CUSTOMFLAG: 'PERMITTED'
    };
    configureEnvironment(env, ['AWS_PUBLIC_CUSTOMFLAG']);
    expect(env.AWS_PUBLIC_CUSTOMFLAG).toBe('PERMITTED');
  });

  it('should remove non-allowed AWS_ vars except endpoint urls (unique keys)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://apiunique.com',
      AWS_ENDPOINT_URL_S3: 'http://apiss3unique.com',
      AWS_TO_REMOVE_FLAG: 'delete_me',
      AWS_ACCESS_KEY_ID: 'AKEY',
      AWS_SECRET_ACCESS_KEY: 'ASECRET',
      AWS_REGION: 'eu-central-3'
    };
    configureEnvironment(env, []);
    expect(env).not.toHaveProperty('AWS_TO_REMOVE_FLAG');
  });

  it('should set credentials if not present (public)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://no-creds-public.com',
      AWS_ENDPOINT_URL_S3: 'http://no-creds-public-s3.com',
    };
    configureEnvironment(env, []);
    expect(env.AWS_ACCESS_KEY_ID).toBe('test');
    expect(env.AWS_SECRET_ACCESS_KEY).toBe('test');
    expect(env.AWS_REGION).toBe('us-east-1');
    expect(env.AWS_DEFAULT_REGION).toBe('us-east-1');
  });

  it('should not override existing credentials and region when allowlisted (unique region)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://cred-region-public.com',
      AWS_ENDPOINT_URL_S3: 'http://cred-region-public-s3.com',
      AWS_ACCESS_KEY_ID: 'EXISTINGID',
      AWS_SECRET_ACCESS_KEY: 'EXISTINGSECRET',
      AWS_REGION: 'us-central-9',
      AWS_DEFAULT_REGION: 'us-central-9'
    };
    configureEnvironment(
      env,
      ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'AWS_DEFAULT_REGION']
    );
    expect(env.AWS_ACCESS_KEY_ID).toBe('EXISTINGID');
    expect(env.AWS_SECRET_ACCESS_KEY).toBe('EXISTINGSECRET');
    expect(env.AWS_REGION).toBe('us-central-9');
    expect(env.AWS_DEFAULT_REGION).toBe('us-central-9');
  });

  it('should override credentials and region when not allowlisted (unique values)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://override-key.com',
      AWS_ENDPOINT_URL_S3: 'http://override-s3.com',
      AWS_ACCESS_KEY_ID: 'OLDCUSTOM',
      AWS_SECRET_ACCESS_KEY: 'OLDCUSTOMSECRET',
      AWS_REGION: 'eu-west-7',
      AWS_DEFAULT_REGION: 'eu-west-7'
    };
    configureEnvironment(env, []);
    expect(env.AWS_ACCESS_KEY_ID).toBe('test');
    expect(env.AWS_SECRET_ACCESS_KEY).toBe('test');
    expect(env.AWS_REGION).toBe('us-east-1');
    expect(env.AWS_DEFAULT_REGION).toBe('us-east-1');
  });

  it('should set endpoints if not present (public)', () => {
    const env = {};
    configureEnvironment(env, []);
    expect(env.AWS_ENDPOINT_URL).toContain('localhost.localstack.cloud');
    expect(env.AWS_ENDPOINT_URL_S3).toContain('s3.localhost.localstack.cloud');
  });

  it('should handle whitespace in allowlist (public)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://whitespace.com',
      AWS_ENDPOINT_URL_S3: 'http://whitespace-s3.com',
      AWS_WHITESPACE_ALLOWED: 'yep'
    };
    configureEnvironment(env, ['  AWS_WHITESPACE_ALLOWED  ']);
    expect(env.AWS_WHITESPACE_ALLOWED).toBe('yep');
  });

  it('should not remove non-AWS_ keys (public)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://nonaws-url.com',
      AWS_ENDPOINT_URL_S3: 'http://nonaws-url-s3.com',
      SOME_OTHER_KEY_PUBLIC: 'SHOULD_KEEP'
    };
    configureEnvironment(env, []);
    expect(env.SOME_OTHER_KEY_PUBLIC).toBe('SHOULD_KEEP');
  });

  it('should not remove AWS_ENDPOINT_URL* keys (public, different suffix)', () => {
    const env = {
      AWS_ENDPOINT_URL: 'http://suffix.com',
      AWS_ENDPOINT_URL_S3: 'http://suffix-s3.com',
      AWS_ENDPOINT_URL_ELASTIC: 'http://elastic-url.com'
    };
    configureEnvironment(env, []);
    expect(env.AWS_ENDPOINT_URL_ELASTIC).toBe('http://elastic-url.com');
  });
});