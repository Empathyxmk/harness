// Karma configuration file, using --headless and --no-sandbox for Chrome in CI/headless/root environment

module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', 'browserify'],
    files: [
      'src/**/*.spec.js'
    ],
    preprocessors: {
      'src/**/*.spec.js': ['browserify']
    },
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: false,
    browsers: ['ChromeNoSandboxHeadless'],
    singleRun: true,
    concurrency: Infinity,
    browserify: {
      debug: true
    },
    customLaunchers: {
      ChromeNoSandboxHeadless: {
        base: 'Chrome',
        flags: ['--no-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage', '--remote-debugging-port=9222']
      }
    }
  });
};