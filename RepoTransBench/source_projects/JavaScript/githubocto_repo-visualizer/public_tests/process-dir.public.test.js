const fs = require('fs');
const { processDir } = require('../src/process-dir');
const shouldExcludePathModule = require('../src/should-exclude-path');

describe('processDir (public)', () => {
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

  it('skips excluded files (public)', async () => {
    // Simulate root containing only "bar", which is excluded
    readdirSyncSpy.mockReturnValue(['bar']);
    statSyncSpy
      .mockImplementationOnce(() => ({ isDirectory: () => true, size: 2 }));
    shouldExcludePathSpy
      .mockImplementation((abs, name) => name === 'bar');

    const tree = await processDir('pubdir', [], []);
    expect(tree).toHaveProperty('name', 'pubdir');
    expect(tree).toHaveProperty('children');
    expect(tree.children).toEqual([]);
  });

  it('recurses directories and files (public)', async () => {
    readdirSyncSpy
      .mockImplementationOnce(() => ['x.txt', 'data'])
      .mockImplementationOnce(() => ['deep.txt']); // for data

    shouldExcludePathSpy.mockImplementation(() => false);
    statSyncSpy
      .mockImplementationOnce(() => ({
        isDirectory: () => true,
        size: 222,
      })) // root
      .mockImplementationOnce(() => ({
        isDirectory: () => false,
        size: 11,
      })) // x.txt
      .mockImplementationOnce(() => ({
        isDirectory: () => true,
        size: 211,
      })) // data
      .mockImplementationOnce(() => ({
        isDirectory: () => false,
        size: 33,
      })); // deep.txt

    const tree = await processDir('/public_root', [], []);
    expect(tree.children.length).toBe(2);
    expect(tree.children[0].name).toBe('x.txt');
    expect(tree.children[1].name).toBe('data');
    expect(tree.children[1].children[0].name).toBe('deep.txt');
  });

  it('returns null on fs.statSync error (public)', async () => {
    statSyncSpy.mockImplementation(() => {
      throw new Error('public fail');
    });
    const node = await processDir('/faildir', [], []);
    expect(node).toBeNull();
  });

  it('handles empty directories (public)', async () => {
    statSyncSpy.mockReturnValueOnce({
      isDirectory: () => true,
      size: 123,
    });
    readdirSyncSpy.mockReturnValueOnce([]);
    shouldExcludePathSpy.mockImplementation(() => false);
    const tree = await processDir('/public_empty', [], []);
    expect(tree.children).toEqual([]);
    expect(tree.name).toBe('public_empty');
    expect(tree.size).toBe(123);
  });

  it('handles regular files (public)', async () => {
    statSyncSpy.mockReturnValueOnce({
      isDirectory: () => false,
      size: 6,
    });
    const tree = await processDir('/myfile', [], []);
    expect(tree.name).toBe('myfile');
    expect(tree.size).toBe(6);
    expect(tree.children).toBeUndefined();
  });
});