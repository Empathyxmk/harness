module.exports = {
  projects: [
    {
      displayName: 'main',
      testMatch: [
        "**/src/**/*.test.js"
      ],
      testPathIgnorePatterns: [
        "/node_modules/"
      ]
    },
    {
      displayName: 'public',
      testMatch: [
        "**/public_tests/**/*.public.test.js"
      ],
      testPathIgnorePatterns: [
        "/node_modules/"
      ]
    }
  ]
}