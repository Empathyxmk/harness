module.exports = {
  testEnvironment: 'node',
  testMatch: [
    "<rootDir>/test/**/*.js"
  ],
  transform: {},
  // Do not transform node_modules (default), but allow usage of require style tests
  coverageDirectory: "./coverage",
  collectCoverageFrom: [
    "index.js"
  ]
}