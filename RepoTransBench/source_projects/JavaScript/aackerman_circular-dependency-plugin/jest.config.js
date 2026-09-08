module.exports = {
  testMatch: [
    "**/__tests__/**/*.test.js",
    "**/public_tests/**/*.public.test.js"
  ],
  testPathIgnorePatterns: [
    "/node_modules/",
    "/__tests__/deps/",
    "/coverage/",
    "/build/"
  ]
};