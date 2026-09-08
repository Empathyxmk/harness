const path = require('path');
jest.resetModules();

let execMock, coreMock, osMock, childProcessExec;

function mockSetup({
    execError = null,
    buildx = 'yes',
    cliExperimental = 'disabled',
    platform = 'darwin',
    arch = 'arm64',
    dockerDaemonJson = '{"debug":true}',
    dockerNightlyVersion = 'nightly-1.0',
    dockerVersion = '20.10.7',
    dockerChannel = 'stable',
    shellStdout = "public_ok",
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
    homedir: jest.fn(() => "/Users/testing"),
  };
  childProcessExec = jest.fn((cmd, cb) => cb(shellError, shellStdout, shellStderr));
  jest.doMock('@actions/exec', () => execMock);
  jest.doMock('@actions/core', () => coreMock);
  jest.doMock('os', () => osMock);
  jest.doMock('child_process', () => ({ exec: childProcessExec }));
}

describe('setup-docker exports (public)', () => {
  beforeEach(() => {
    mockSetup();
  });

  it('should have the right exports', () => {
    const mod = require('../lib/setup-docker');
    expect(typeof mod.shell).toBe('function');
    expect(typeof mod.buildx).toBe('function');
    expect(typeof mod.run).toBe('function');
  });
});

describe('shell (public)', () => {
  beforeEach(() => {
    mockSetup({ shellStdout: "output for pub", shellStderr: "", shellError: null });
  });

  it('resolves with stdout (public)', async () => {
    const { shell } = require('../lib/setup-docker');
    const out = await shell('pwd');
    expect(out).toBe("output for pub");
    expect(childProcessExec).toHaveBeenCalled();
  });

  it('rejects on error (public)', async () => {
    mockSetup({ shellError: new Error('public fail') });
    const { shell } = require('../lib/setup-docker');
    await expect(shell('pwd')).rejects.toThrow('public fail');
  });

  it('rejects on stderr (public)', async () => {
    mockSetup({ shellStdout: "directory", shellStderr: "something went wrong!" });
    const { shell } = require('../lib/setup-docker');
    await expect(shell('pwd')).rejects.toBe("something went wrong!");
  });
});

describe('buildx (public)', () => {
  it('should run buildx and set cli experimental (public)', async () => {
    mockSetup({ buildx: 'true', cliExperimental: 'disabled' }); // different cliExperimental
    const { buildx } = require('../lib/setup-docker');
    await buildx();
    expect(execMock.exec).toHaveBeenCalled();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CLI_EXPERIMENTAL', 'disabled');
  });

  it('does not run buildx install if buildx set to off', async () => {
    mockSetup({ buildx: 'off' });
    const { buildx } = require('../lib/setup-docker');
    await buildx();
    expect(coreMock.info).toHaveBeenCalledWith('buildx disabled');
  });

  it('falls back if buildx version throws (public)', async () => {
    mockSetup({ buildx: 'true', execError: new Error('public-exec-fail') });
    const { buildx } = require('../lib/setup-docker');
    await buildx();
    expect(coreMock.info).toHaveBeenCalledWith('this docker version NOT Support Buildx');
  });
});

describe('run (public)', () => {
  it('should handle sunos as a different platform', async () => {
    mockSetup({ platform: 'sunos' });
    const { run } = require('../lib/setup-docker');
    await run();
    expect(coreMock.debug).toHaveBeenCalledWith('check platform');
    expect(execMock.exec).toHaveBeenCalledWith('echo', expect.any(Array));
  });

  it('should warn if macos but arch is ia32', async () => {
    mockSetup({ platform: 'darwin', arch: 'ia32' });
    const { run } = require('../lib/setup-docker');
    await run();
    expect(coreMock.warning).toHaveBeenCalledWith('only support macOS x86_64, os arch is ia32');
  });

  it('should set up docker on macOS x64 (ROOT DIR)', async () => {
    mockSetup({ platform: 'darwin', arch: 'x64' });
    const { run } = require('../lib/setup-docker');
    await run();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CONFIG', '/Users/testing/.docker');
    expect(execMock.exec).toHaveBeenCalledWith('wget', [
      'https://raw.githubusercontent.com/Homebrew/homebrew-cask/fe866ec0765de141599745f03e215452db7f511b/Casks/docker.rb'
    ]);
  });

  it('should not warn or debug for freebsd', async () => {
    mockSetup({ platform: 'freebsd', arch: 'x64' });
    const { run } = require('../lib/setup-docker');
    await run();
    expect(coreMock.debug).not.toHaveBeenCalledWith('check platform');
    expect(coreMock.warning).not.toHaveBeenCalled();
  });
});

describe('buildx public input cases', () => {
  it('should still export cli experimental if cliExperimental is missing (public)', async () => {
    mockSetup({ buildx: 'true', cliExperimental: undefined });
    const { buildx } = require('../lib/setup-docker');
    await buildx();
    expect(coreMock.exportVariable).toHaveBeenCalledWith('DOCKER_CLI_EXPERIMENTAL', 'enabled');
  });

  it('should process buildx input as enabled (not true)', async () => {
    mockSetup({ buildx: 'enabled', cliExperimental: 'enabled' });
    const { buildx } = require('../lib/setup-docker');
    await buildx();
    expect(coreMock.info).toHaveBeenCalledWith('buildx disabled');
  });
});

// The most-meaningful and relevant test cases adapted to new input data.