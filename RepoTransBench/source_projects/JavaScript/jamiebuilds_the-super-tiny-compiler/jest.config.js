module.exports = {
  testEnvironment: "node",
  testMatch: [
    "**/__tests__/**/*.js?(x)",
    "**/?(*.)+(spec|test).js?(x)"
  ],
  collectCoverage: true,
  coverageReporters: ["text", "html"],
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "/test\\.js$" // ignore the legacy hand-rolled test file
  ],
};