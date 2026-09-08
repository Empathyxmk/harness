// --- constants ---
const EDGE_PORT = process.env.EDGE_PORT
  ? Number(process.env.EDGE_PORT)
  : 4566;

const PROTOCOL = process.env.USE_SSL === "1" || process.env.USE_SSL === "true" ? "https" : "http";

// --- helpers ---
function isEnvTrue(envOrKey, keyMaybe) {
  // Support legacy and public test usage
  if (typeof envOrKey === 'string' && typeof keyMaybe === 'undefined') {
    // Looks like key name only, so check process.env
    const key = envOrKey;
    return (
      process.env[key] === true ||
      process.env[key] === "true" ||
      process.env[key] === 1 ||
      process.env[key] === "1"
    );
  } else if (
    typeof envOrKey === 'object' &&
    envOrKey !== null &&
    typeof keyMaybe === 'string' &&
    keyMaybe !== ''
  ) {
    // Env provided explicitly
    if (!(keyMaybe in envOrKey)) return false;
    const val = envOrKey[keyMaybe];
    return val === true || val === "true" || val === 1 || val === "1";
  }
  return false;
}

// --- error class ---
class EnvironmentMisconfigurationError extends Error {
  constructor(msg) {
    super(msg);
    this.name = "EnvironmentMisconfigurationError";
  }
}

// --- main logic ---
/**
 * Mutates env in place.
 * @param {object} env
 * @param {array|string} [explicitAllowList]
 */
function configureEnvironment(env, explicitAllowList) {
  // 1. parse AWS_ENVAR_ALLOWLIST to extract the keys we should allow
  let allowListStr = explicitAllowList;
  if (typeof allowListStr === "undefined" || allowListStr === null) {
    allowListStr = process.env.AWS_ENVAR_ALLOWLIST || "";
    if (allowListStr === "") allowListStr = [];
    else allowListStr = allowListStr.split(",").map((item) => item.trim());
  }
  if (Array.isArray(allowListStr)) {
    // sanitize/trim array values
    allowListStr = allowListStr.map((item) => (typeof item === "string" ? item.trim() : item));
  } else if (typeof allowListStr === "string") {
    allowListStr = allowListStr.split(",").map((item) => item.trim());
  } else {
    allowListStr = [];
  }
  const allowList = Array.from(new Set(allowListStr));

  // 2. build array of keys to remove
  const keysToRemove = Object.keys(env).filter((key) => {
    if (!key.startsWith("AWS_")) return false;
    if (key.startsWith("AWS_ENDPOINT_URL")) return false;
    if (allowList.includes(key)) return false;
    return true;
  });

  keysToRemove.forEach((key) => {
    delete env[key];
  });

  // 3. endpoints: must BOTH be present if either is
  const endpoints = ['AWS_ENDPOINT_URL', 'AWS_ENDPOINT_URL_S3'];
  const endpointsPresent = endpoints.map((ep) => ep in env);
  if (endpointsPresent.includes(true) && !endpointsPresent.every(Boolean)) {
    throw new EnvironmentMisconfigurationError(
      "If specifying 'AWS_ENDPOINT_URL' then 'AWS_ENDPOINT_URL_S3' must be specified"
    );
  }

  // 4. credentials & region
  const envarDefaults = {
    AWS_ACCESS_KEY_ID: "test",
    AWS_SECRET_ACCESS_KEY: "test",
    AWS_REGION: "us-east-1",
    AWS_DEFAULT_REGION: "us-east-1"
  };
  Object.entries(envarDefaults).forEach(([key, val]) => {
    // Only fill if not explicitly allowlisted
    if (allowList.includes(key)) return;
    env[key] = val;
  });

  // 5. endpoints default
  if (!env.AWS_ENDPOINT_URL) {
    // prefer "localhost.localstack.cloud" (legacy fallback to http://localhost:4566)
    env.AWS_ENDPOINT_URL = "http://localhost.localstack.cloud:4566";
  }
  if (!env.AWS_ENDPOINT_URL_S3) {
    env.AWS_ENDPOINT_URL_S3 = "http://s3.localhost.localstack.cloud:4566";
  }
}

// --- exports ---
module.exports = {
  isEnvTrue,
  EDGE_PORT,
  PROTOCOL,
  EnvironmentMisconfigurationError,
  configureEnvironment,
};