module.exports = {
  roots: ["<rootDir>/spec"],
  transform: {
    "^.+\\.js$": "babel-jest"
  },
  testEnvironment: "node",
  coverageDirectory: "coverage",
  collectCoverageFrom: [
    "src/**/*.js"
  ]
};