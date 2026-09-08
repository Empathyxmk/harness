const {
  isEnvTrue,
  EDGE_PORT,
  PROTOCOL,
  configureEnvironment,
  EnvironmentMisconfigurationError,
} = require("../src/index");

describe("isEnvTrue", () => {
  const OLD_ENV = process.env;

  beforeEach(() => {
    process.env = { ...OLD_ENV };
  });

  afterAll(() => {
    process.env = OLD_ENV;
  });

  it("should return true for environment variable set to '1'", () => {
    process.env.TEST_ENV = "1";
    expect(isEnvTrue("TEST_ENV")).toBe(true);
  });

  it("should return true for environment variable set to 'true'", () => {
    process.env.TEST_ENV = "true";
    expect(isEnvTrue("TEST_ENV")).toBe(true);
  });

  it("should return false for environment variable set to other value", () => {
    process.env.TEST_ENV = "yes";
    expect(isEnvTrue("TEST_ENV")).toBe(false);
  });

  it("should return false for unset environment variable", () => {
    delete process.env.TEST_ENV;
    expect(isEnvTrue("TEST_ENV")).toBe(false);
  });
});

describe("constants", () => {
  it("EDGE_PORT - default", () => {
    expect(EDGE_PORT).toBe(4566);
  });

  it("PROTOCOL should be http if USE_SSL is not set", () => {
    expect(PROTOCOL).toBe("http");
  });
});

describe("EnvironmentMisconfigurationError", () => {
  it("should be instance of Error", () => {
    const err = new EnvironmentMisconfigurationError("test");
    expect(err).toBeInstanceOf(Error);
    expect(err.message).toBe("test");
  });
});

describe("configureEnvironment", () => {
  let env;

  beforeEach(() => {
    env = {
      AWS_FOO: "foo",
      AWS_BAR: "bar",
      AWS_ENDPOINT_URL: "some_url",
      AWS_ENDPOINT_URL_S3: "some_url_s3",
    };
  });

  it("should throw if AWS_ENDPOINT_URL set but not AWS_ENDPOINT_URL_S3", () => {
    delete env.AWS_ENDPOINT_URL_S3;
    expect(() =>
      configureEnvironment({ ...env }, "")
    ).toThrow(EnvironmentMisconfigurationError);
  });

  it("should not throw if both AWS_ENDPOINT_URL and AWS_ENDPOINT_URL_S3 set", () => {
    expect(() =>
      configureEnvironment({ ...env }, "")
    ).not.toThrow();
  });

  it("should allow allowlisted AWS_ vars", () => {
    env.AWS_SECRET_THING = "y";
    configureEnvironment(env, "AWS_SECRET_THING");
    expect(env.AWS_SECRET_THING).toBe("y");
  });

  it("should remove non-allowed AWS_ vars except endpoint urls", () => {
    env.AWS_FOO = "foo";
    env.AWS_BAR = "bar";
    configureEnvironment(env, "");
    // AWS_ENDPOINT_URL and AWS_ENDPOINT_URL_S3 should survive
    expect(env.AWS_ENDPOINT_URL).toBeDefined();
    expect(env.AWS_ENDPOINT_URL_S3).toBeDefined();
    expect(env.AWS_FOO).toBeUndefined();
    expect(env.AWS_BAR).toBeUndefined();
  });

  it("should set credentials if not present", () => {
    const emptyEnv = {};
    configureEnvironment(emptyEnv, "");
    expect(emptyEnv.AWS_ACCESS_KEY_ID).toBe("test");
    expect(emptyEnv.AWS_SECRET_ACCESS_KEY).toBe("test");
    expect(emptyEnv.AWS_REGION).toBe("us-east-1");
    expect(emptyEnv.AWS_DEFAULT_REGION).toBe("us-east-1");
  });

  it("should not override existing credentials and region when allowlisted", () => {
    env.AWS_ACCESS_KEY_ID = "foo";
    env.AWS_SECRET_ACCESS_KEY = "bar";
    env.AWS_REGION = "ca-central-1";
    env.AWS_DEFAULT_REGION = "eu-west-2";
    // The implementation *always* sets those fields if present, so to not override, they must be allowlisted
    configureEnvironment(env, "AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_REGION,AWS_DEFAULT_REGION");
    expect(env.AWS_ACCESS_KEY_ID).toBe("foo");
    expect(env.AWS_SECRET_ACCESS_KEY).toBe("bar");
    expect(env.AWS_REGION).toBe("ca-central-1");
    expect(env.AWS_DEFAULT_REGION).toBe("eu-west-2");
  });

  it("should override credentials and region when not allowlisted", () => {
    env.AWS_ACCESS_KEY_ID = "foo";
    env.AWS_SECRET_ACCESS_KEY = "bar";
    env.AWS_REGION = "ca-central-1";
    env.AWS_DEFAULT_REGION = "eu-west-2";
    configureEnvironment(env, "");
    expect(env.AWS_ACCESS_KEY_ID).toBe("test");
    expect(env.AWS_SECRET_ACCESS_KEY).toBe("test");
    expect(env.AWS_REGION).toBe("us-east-1");
    expect(env.AWS_DEFAULT_REGION).toBe("us-east-1");
  });

  it("should set endpoints if not present", () => {
    const emptyEnv = {};
    configureEnvironment(emptyEnv, "");
    expect(emptyEnv.AWS_ENDPOINT_URL).toContain("localhost.localstack.cloud");
    expect(emptyEnv.AWS_ENDPOINT_URL_S3).toContain("s3.localhost.localstack.cloud");
  });

  it("should handle whitespace in allowlist", () => {
    env.AWS_KEY1 = "val1";
    env.AWS_KEY2 = "val2";
    configureEnvironment(env, "  AWS_KEY1 , AWS_KEY2  ");
    expect(env.AWS_KEY1).toBe("val1");
    expect(env.AWS_KEY2).toBe("val2");
  });

  it("should not remove non-AWS_ keys", () => {
    env.NOT_AWS = "will-live";
    configureEnvironment(env, "");
    expect(env.NOT_AWS).toEqual("will-live");
  });

  it("should not remove AWS_ENDPOINT_URL* keys", () => {
    env.AWS_ENDPOINT_URL_CUSTOM = "x";
    configureEnvironment(env, "");
    expect(env.AWS_ENDPOINT_URL_CUSTOM).toBe("x");
  });
});