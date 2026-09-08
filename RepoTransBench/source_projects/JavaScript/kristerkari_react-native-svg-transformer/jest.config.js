module.exports = {
  testEnvironment: "node",
  collectCoverage: true,
  collectCoverageFrom: [
    "index.js",
    "expo/index.js",
    "react-native/index.js"
  ],
  coverageReporters: ["text", "html"]
};