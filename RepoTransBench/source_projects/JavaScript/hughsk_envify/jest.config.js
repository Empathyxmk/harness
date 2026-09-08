module.exports = {
  testMatch: [
    "**/*.test.js"
  ],
  testPathIgnorePatterns: [
    "/node_modules/",
    "<rootDir>/test.js" // Ignore legacy tape test
  ],
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "<rootDir>/test.js"
  ]
};