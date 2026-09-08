module.exports = {
  testEnvironment: "node",
  testMatch: [
    "<rootDir>/test/**/*.jest.js"
  ],
  collectCoverage: true,
  collectCoverageFrom: [
    "src/**/*.js",
    "!src/index.js"
  ],
  coverageReporters: ["text", "html"]
};