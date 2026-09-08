module.exports = {
  roots: [
    "<rootDir>/src",
    "<rootDir>/src/tests"
  ],
  testMatch: [
    "**/?(*.)+(spec|test).[jt]s?(x)"
  ],
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest"
  },
  collectCoverageFrom: [
    "src/**/*.{js,jsx}",
    "!src/tests/**"
  ],
  coverageReporters: ["text", "html"]
};