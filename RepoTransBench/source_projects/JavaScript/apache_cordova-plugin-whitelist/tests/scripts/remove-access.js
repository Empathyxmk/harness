// Minimal implementation to allow the test to run, can be expanded based on test requirements.
// This script is supposed to remove <access origin="*" /> from config.xml in Cordova plugin projects.

const fs = require('fs');
const path = require('path');

const configPath = path.join(process.cwd(), 'config.xml');

fs.readFile(configPath, 'utf8', (err, data) => {
    if (err) {
        console.log('Error reading config.xml:', err.message);
        return;
    }
    const newData = data.replace(/<access\s+origin="\*"\s*\/?>/g, '');
    fs.writeFile(configPath, newData, (err) => {
        if (err) {
            console.log('Error writing config.xml:', err.message);
        } else {
            console.log('<access origin="*" /> removed from config.xml');
        }
    });
});