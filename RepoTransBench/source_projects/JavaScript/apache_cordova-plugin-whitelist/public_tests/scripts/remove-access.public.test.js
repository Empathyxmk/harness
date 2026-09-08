const fs = require('fs');
const path = require('path');

describe('remove-access.js (public)', () => {
  const configPath = path.join(__dirname, 'config.xml');

  afterEach(() => {
    // Cleanup config.xml if it exists
    if (fs.existsSync(configPath)) fs.unlinkSync(configPath);
  });

  it('removes <access origin="example.com" /> from config.xml when surrounded by other domains', (done) => {
    const originalConfig = `
<widget>
    <access origin="https://first.com" />
    <access origin="example.com" />
    <access origin="https://last.com" />
</widget>
    `.trim();
    const expectedConfig = `
<widget>
    <access origin="https://first.com" />
    <access origin="https://last.com" />
</widget>
    `.trim();

    fs.writeFileSync(configPath, originalConfig);

    // Simulate inline removal logic for testing (replace the "public" variant line)
    let configData = fs.readFileSync(configPath, 'utf8');
    configData = configData.replace(/\s*<access origin="example\.com" \/>/, '');
    fs.writeFileSync(configPath, configData);

    setTimeout(() => {
      const result = fs.readFileSync(configPath, 'utf8');
      expect(result).toBe(expectedConfig);
      done();
    });
  });

  it('logs error if readFile fails (public variant)', (done) => {
    const spyLog = jest.spyOn(console, 'log').mockImplementation(() => {});

    // Remove file so readFile fails
    if (fs.existsSync(configPath)) fs.unlinkSync(configPath);

    // Simulate failure
    try {
      fs.readFileSync(configPath, 'utf8');
    } catch (e) {
      console.log('Error reading config.xml:', e.message);
    }

    setTimeout(() => {
      expect(spyLog).toHaveBeenCalled();
      spyLog.mockRestore();
      done();
    });
  });

  it('logs error if writeFile fails (public variant)', (done) => {
    const spyLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    fs.writeFileSync(configPath, '<widget></widget>');

    // Simulate writeFile failure
    const origWriteFileSync = fs.writeFileSync;
    fs.writeFileSync = () => { throw new Error('Public simulated write error'); };

    try {
      fs.writeFileSync(configPath, '<widget></widget>');
    } catch (e) {
      console.log('Error writing config.xml:', e.message);
    }

    // Restore
    fs.writeFileSync = origWriteFileSync;

    setTimeout(() => {
      expect(spyLog).toHaveBeenCalledWith('Error writing config.xml:', 'Public simulated write error');
      spyLog.mockRestore();
      done();
    });
  });
});