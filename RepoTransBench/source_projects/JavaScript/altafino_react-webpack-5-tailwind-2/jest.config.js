module.exports = {
  testEnvironment: "node", // Use "node" to avoid the 'testEnvironmentOptions' JSDOM bug
  moduleNameMapper: {
    "\\.(css|scss)$": "identity-obj-proxy",
    "\\.(svg|png|jpg|jpeg|gif)$": "<rootDir>/__mocks__/fileMock.js"
  }
};