module.exports = {
  testEnvironment: "node",
  transform: {
    "^.+\\.js$": "babel-jest"
  },
  moduleFileExtensions: [
    "js"
  ],
  // Ignore node_modules explicitly
  transformIgnorePatterns: ["/node_modules/"]
};