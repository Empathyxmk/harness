module.exports = {
  testEnvironment: "node",
  collectCoverage: true,
  coverageReporters: ["text", "html"],
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "index.d.ts",
    "readme.md",
    "logo.png",
    "playground-small.jpg",
    "LICENSE",
    "package.json",
    "package-lock.json"
  ]
};