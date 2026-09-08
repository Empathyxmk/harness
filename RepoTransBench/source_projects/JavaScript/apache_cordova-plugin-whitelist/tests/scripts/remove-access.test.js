/**
 * @jest-environment node
 */
const fs = require('fs');
const path = require('path');

const configPath = path.join(process.cwd(), 'config.xml');
const origConfig = '<widget><access origin="*" /><access origin="something.com" /></widget>';
const removedConfig = '<widget><access origin="something.com" /></widget>';

describe('remove-access.js', () => {
  beforeEach(() => {
    // Clean up config.xml, write fresh original content
    if (fs.existsSync(configPath)) {
      fs.unlinkSync(configPath);
    }
    fs.writeFileSync(configPath, origConfig, 'utf8');
    jest.resetModules();
  });

  afterAll(() => {
    // Clean up
    if (fs.existsSync(configPath)) {
      fs.unlinkSync(configPath);
    }
  });

  it('removes <access origin="*" /> from config.xml (normal flow)', (done) => {
    const spyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    require('./remove-access.js');
    setTimeout(() => {
      const result = fs.readFileSync(configPath, 'utf8');
      expect(result).toBe(removedConfig);
      expect(spyLog).toHaveBeenCalledWith('<access origin="*" /> removed from config.xml');
      spyLog.mockRestore();
      done();
    }, 100);
  });

  it('logs error if readFile fails', (done) => {
    const spyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    // Remove file so readFile fails
    fs.unlinkSync(configPath);
    require('./remove-access.js');
    setTimeout(() => {
      expect(spyLog).toHaveBeenCalled();
      spyLog.mockRestore();
      done();
    }, 100);
  });

  it('logs error if writeFile fails', (done) => {
    const spyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    // Patch fs.writeFile to simulate error
    const origWriteFile = fs.writeFile;
    fs.writeFile = (p, d, cb) => cb(new Error('Simulated write error'));
    require('./remove-access.js');
    setTimeout(() => {
      expect(spyLog).toHaveBeenCalledWith('Error writing config.xml:', 'Simulated write error');
      spyLog.mockRestore();
      fs.writeFile = origWriteFile;
      done();
    }, 100);
  });
});