// Existing imports and mocking utilities remain
const path = require('path');
jest.resetModules();

let execMock, coreMock, osMock, childProcessExec;

function mockSetup({
    execError = null,
    buildx = 'true',
    cliExperimental = 'enabled',
    platform = 'linux',
    arch = 'x64',
    dockerDaemonJson = '{}',
    dockerNightlyVersion = '',
    dockerVersion = '',
    dockerChannel = '',
    shellStdout = "ok",
    shellStderr = "",
    shellError = null,
} = {}) {
  jest.resetModules();
  execMock = {
    exec: jest.fn().mockImplementation((cmd, args, opts) => {
      if (execError) return Promise.reject(execError);
      return Promise.resolve(0);
    }),
  };
  coreMock = {
    getInput: jest.fn((name) => {
      switch (name) {
        case 'docker_version': return dockerVersion;
        case 'docker_channel': return dockerChannel;
        case 'docker_cli_experimental': return cliExperimental;
        case 'docker_buildx': return buildx;
        case 'docker_daemon_json': return dockerDaemonJson;
        case 'docker_nightly_version': return dockerNightlyVersion;
        default: return '';
      }
    }),
    exportVariable: jest.fn(),
    debug: jest.fn(),
    startGroup: jest.fn(),
    endGroup: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
  };
  osMock = {
    platform: jest.fn(() => platform),
    arch: jest.fn(() => arch),
    homedir: jest.fn(() => "/Users/runner"),
  };
  childProcessExec = jest.fn((cmd, cb) => cb(shellError, shellStdout, shellStderr));
  jest.doMock('@actions/exec', () => execMock);
  jest.doMock('@actions/core', () => coreMock);
  jest.doMock('os', () => osMock);
  jest.doMock('child_process', () => ({ exec: childProcessExec }));
}

describe('setup-docker exports', () => {
  beforeEach(() => {
    mockSetup();
  });

  it('exports shell, buildx, run', () => {
    const mod = require('./setup-docker');
    expect(typeof mod.shell).toBe('function');
    expect(typeof mod.buildx).toBe('function');
    expect(typeof mod.run).toBe('function');
  });
});

describe('shell', () => {
  beforeEach(() => {
    mockSetup({ shellStdout: "out", shellStderr: "", shellError: null });
  });

  it('should resolve with stdout', async () => {
    const { shell } = require('./setup-docker');
    const out = await shell('ls');
    expect(out).toBe("out");
    expect(childProcessExec).toHaveBeenCalled();
  });

  it('should reject on error', async () => {
    mockSetup({ shellError: new Error('fail') });
    const { shell } = require('./setup-docker');
    await expect(shell('ls')).rejects.toThrow('fail');
  });

  it('should reject on stderr', async () => {
    mockSetup({ shellStdout: "foo", shellStderr: "err here" });
    const { shell } = require('./setup-docker');
    await expect(shell('ls')).rejects.toBe("err here");
  });
});

describe('buildx', () => {
  it('should run buildx and set cli experimental (call is first)', async () => {
    mockSetup({ buildx: 'true', cliExperimental: 'enabled' });
    const { buildx } = require('./setup-docker');
    await buildx();
    // We need to check that execMock.exec was called at least once
    expect(execMock.exec).toHaveBeenCalled();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CLI_EXPERIMENTAL', 'enabled');
  });

  it('does not run buildx install if buildx not true', async () => {
    mockSetup({ buildx: 'false' });
    const { buildx } = require('./setup-docker');
    await buildx();
    expect(coreMock.info).toHaveBeenCalledWith('buildx disabled');
  });

  it('falls back if buildx version fails', async () => {
    mockSetup({ buildx: 'true', execError: Error('fail') });
    const { buildx } = require('./setup-docker');
    await buildx();
    expect(coreMock.info).toHaveBeenCalledWith('this docker version NOT Support Buildx');
  });
});

describe('run', () => {
  it('should error if windows (win32) platform', async () => {
    mockSetup({ platform: 'win32' });
    const { run } = require('./setup-docker');
    await run();
    expect(coreMock.debug).toHaveBeenCalledWith('check platform');
    expect(execMock.exec).toHaveBeenCalledWith('echo', expect.any(Array));
  });

  it('should warn if macos but arch not x64', async () => {
    mockSetup({ platform: 'darwin', arch: 'arm64' });
    const { run } = require('./setup-docker');
    await run();
    expect(coreMock.warning).toHaveBeenCalledWith('only support macOS x86_64, os arch is arm64');
  });

  it('should set up docker on macOS x64', async () => {
    mockSetup({ platform: 'darwin', arch: 'x64' });
    const { run } = require('./setup-docker');
    await run();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CONFIG', '/Users/runner/.docker');
    expect(execMock.exec).toHaveBeenCalledWith('wget', [
      'https://raw.githubusercontent.com/Homebrew/homebrew-cask/fe866ec0765de141599745f03e215452db7f511b/Casks/docker.rb'
    ]);
  });

  it('should not do anything special for linux', async () => {
    mockSetup({ platform: 'linux', arch: 'x64' });
    const { run } = require('./setup-docker');
    await run();
    expect(coreMock.debug).not.toHaveBeenCalledWith('check platform');
    expect(coreMock.warning).not.toHaveBeenCalled();
  });
});

// New edge case tests for more coverage:

describe('buildx additional input cases', () => {
  it('should still export cli experimental if value is missing', async () => {
    mockSetup({ buildx: 'true', cliExperimental: '' });
    const { buildx } = require('./setup-docker');
    await buildx();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CLI_EXPERIMENTAL', 'enabled');
  });

  it('should process when buildx input is not exactly true', async () => {
    mockSetup({ buildx: '1', cliExperimental: 'enabled' });
    const { buildx } = require('./setup-docker');
    await buildx();
    // Should not trigger buildx install, should see "buildx disabled" instead
    // Actually, in code only ('true' === 'true') passes, this is an exclusion edge
    expect(coreMock.info).toHaveBeenCalledWith('buildx disabled');
  });
});

describe('run more edge cases', () => {
  it('should call all macOS steps', async () => {
    mockSetup({ platform: 'darwin', arch: 'x64', dockerDaemonJson: '{"debug":true}' });
    const { run } = require('./setup-docker');
    await run();
    expect(execMock.exec).toHaveBeenCalledWith('cat', [
      '/Users/runner/.docker/daemon.json',
    ]);
  });
});