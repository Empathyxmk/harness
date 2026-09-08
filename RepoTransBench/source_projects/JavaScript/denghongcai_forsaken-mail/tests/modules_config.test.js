// Remove incorrect fs mocking, use real test files instead for accuracy

const path = require('path');
const fs = require('fs');

const TEST_JSON = path.join(process.cwd(), 'config-default.json');
const TEST_JS = path.join(process.cwd(), 'config-default.js');
const BACKUP_JSON = path.join(process.cwd(), 'config-default.json.bak');
const BACKUP_JS = path.join(process.cwd(), 'config-default.js.bak');

// Utility to backup config files if present
function backupFile(src, backup) {
  if (fs.existsSync(src)) fs.renameSync(src, backup);
}
function restoreFile(src, backup) {
  if (fs.existsSync(backup)) fs.renameSync(backup, src);
}
// Utility to remove file if exists
function rm(file) { if (fs.existsSync(file)) fs.unlinkSync(file); }

describe('modules/config.js integration (real file existence)', () => {
  beforeEach(() => {
    // backup
    backupFile(TEST_JSON, BACKUP_JSON);
    backupFile(TEST_JS, BACKUP_JS);
    rm(TEST_JSON);
    rm(TEST_JS);
    jest.resetModules();
  });

  afterEach(() => {
    // cleanup and restore
    rm(TEST_JSON);
    rm(TEST_JS);
    restoreFile(TEST_JSON, BACKUP_JSON);
    restoreFile(TEST_JS, BACKUP_JS);
    jest.resetModules();
  });

  test('Loads JSON config if config-default.json exists', () => {
    fs.writeFileSync(TEST_JSON, JSON.stringify({ test: 'ok', keywordBlackList: ['yes'] }));
    const config = require('../modules/config');
    expect(config.test).toBe('ok');
    expect(config.keywordBlackList).toEqual(['yes']);
  });

  test('Falls back to JS config if config-default.json does not exist, and config-default.js exists', () => {
    fs.writeFileSync(TEST_JS, 'module.exports = { test2: "hi", keywordBlackList: ["hello"] };');
    const config = require('../modules/config');
    expect(config.test2).toBe('hi');
    expect(config.keywordBlackList).toEqual(['hello']);
  });

  test('Throws if neither config file exists', () => {
    expect(() => require('../modules/config')).toThrow();
  });
});