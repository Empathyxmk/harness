module.exports = {
  testMatch: [
    "**/*.test.js",
    "**/test.js"
  ],
  collectCoverage: true,
  collectCoverageFrom: [
    "index.js"
  ],
  coverageReporters: ["text", "html"]
};