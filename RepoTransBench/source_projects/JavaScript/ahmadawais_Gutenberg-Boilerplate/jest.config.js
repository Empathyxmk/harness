module.exports = {
  testEnvironment: "jsdom",
  roots: [
    "<rootDir>/block"
  ],
  moduleFileExtensions: ["js", "jsx"],
  transform: {
    "^.+\\.jsx?$": "babel-jest"
  }
};