export default {
  testMatch: [
    "**/test/**/*.test.js",
    "**/public_tests/**/*.public.test.js"
  ],
  transform: {},
  extensionsToTreatAsEsm: [".js"],
  testEnvironment: "node",
  moduleFileExtensions: ["js", "json", "node"],
};