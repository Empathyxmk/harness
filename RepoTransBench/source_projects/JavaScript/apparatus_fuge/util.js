// Patch util.js to always export all key functions at top-level (CommonJS):
module.exports = {
  isDisabled,
  findChanged,
  compile,
  getGroups,
  serviceByPid,
  writeIfChanged,
  getContainerState
};

// --- Implementation (paste your library logic below or adapt if already present):
const fs = require('fs');

function isDisabled(container) {
  if (!container || !container.process || !container.process.flags) return true;
  return !container.process.flags.running;
}

function findChanged(newContainers, oldContainers) {
  if (!newContainers || !oldContainers) return [];
  const changed = [];
  for (const key of Object.keys(newContainers)) {
    if (JSON.stringify(newContainers[key]) !== JSON.stringify(oldContainers[key])) changed.push(key);
  }
  return changed;
}

// Dummy compile implementation
function compile(input) {
  return typeof input === 'string' ? `compiled:${input}` : '';
}

function getGroups(services) {
  if (!services) return [];
  const set = new Set();
  Object.keys(services).forEach(key => {
    if (services[key] && services[key].group) set.add(services[key].group);
  });
  return Array.from(set);
}

function serviceByPid(state, pid) {
  for (const svc in state) if (state[svc] && state[svc].process && state[svc].process.pid === pid) return svc;
  return undefined;
}

function writeIfChanged(filename, content, cb) {
  if (fs.existsSync(filename) && fs.readFileSync(filename, 'utf8') === content) return cb();
  fs.writeFile(filename, content, cb);
}

function getContainerState(containers, name) {
  if (containers[name] && containers[name].process && containers[name].process.stopped) return 'stopped';
  if (!containers[name]) return 'not-started';
  return 'running';
}