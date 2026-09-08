// PATCH 4: Fix logic for skipping excluded directories in "skips excluded files" test

const fs = require('fs');
const { processDir } = require('./process-dir');
const shouldExcludePathModule = require('./should-exclude-path');

describe('processDir', () => {
  let readdirSyncSpy, statSyncSpy, shouldExcludePathSpy;

  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    readdirSyncSpy = jest.spyOn(fs, 'readdirSync');
    statSyncSpy = jest.spyOn(fs, 'statSync');
    shouldExcludePathSpy = jest.spyOn(shouldExcludePathModule, 'shouldExcludePath');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('skips excluded files', async () => {
    // Simulate a root directory containing only one folder "foo", which is excluded
    readdirSyncSpy.mockReturnValue(['foo']);
    // Always return root as a directory so processDir will try to recurse
    statSyncSpy
      .mockImplementationOnce(() => ({ isDirectory: () => true, size: 1 })) // root dir
      // For "foo", we may not even call statSync if shouldExcludePath returns true before that
      ;
    // Exclude path for "foo"
    shouldExcludePathSpy
      .mockImplementation((abs, name) => name === 'foo');

    const tree = await processDir('testdir', [], []);
    // The returned tree node is for the root 'testdir', which always exists,
    // but children[] should be empty if all entries are excluded
    expect(tree).toHaveProperty('name', 'testdir');
    expect(tree)
      .toHaveProperty('children');
    expect(tree.children).toEqual([]); // Correct: all children were excluded
  });

  it('recurses directories and files', async () => {
    readdirSyncSpy
      .mockImplementationOnce(() => ['file1', 'dir2']) // for root
      .mockImplementationOnce(() => []); // for dir2
    shouldExcludePathSpy
      .mockImplementation(() => false);
    statSyncSpy
      .mockImplementationOnce(() => ({
        isDirectory: () => true,
        size: 100,
      })) // root dir
      .mockImplementationOnce(() => ({
        isDirectory: () => false,
        size: 10,
      })) // file1
      .mockImplementationOnce(() => ({
        isDirectory: () => true,
        size: 90,
      })); // dir2
    const tree = await processDir('/root', [], []);
    expect(tree.children.length).toBe(2);
    expect(tree.children[0].name).toBe('file1');
    expect(tree.children[1].name).toBe('dir2');
    expect(tree.children[1].children.length).toBe(0);
  });

  it('returns null on fs.statSync error', async () => {
    statSyncSpy.mockImplementation(() => {
      throw new Error('fail');
    });
    const node = await processDir('/bad', [], []);
    expect(node).toBeNull();
  });

  it('handles empty directories', async () => {
    statSyncSpy.mockReturnValueOnce({
      isDirectory: () => true,
      size: 42,
    });
    readdirSyncSpy.mockReturnValueOnce([]);
    shouldExcludePathSpy.mockImplementation(() => false);
    const tree = await processDir('/emptydir', [], []);
    expect(tree.children).toEqual([]);
    expect(tree.name).toBe('emptydir');
    expect(tree.size).toBe(42);
  });

  it('handles regular files', async () => {
    statSyncSpy.mockReturnValueOnce({
      isDirectory: () => false,
      size: 8,
    });
    const tree = await processDir('/file', [], []);
    expect(tree.name).toBe('file');
    expect(tree.size).toBe(8);
    expect(tree.children).toBeUndefined();
  });
});