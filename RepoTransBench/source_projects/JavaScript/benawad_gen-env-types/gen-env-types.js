function sanitizeKey(key) {
  // Only allow valid TS/JS identifier names (letters, numbers, underscores, not starting with number)
  if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(key)) return key;
  return null;
}

function generateEnvTypes(dotenvText) {
  // Split by lines, parse env keys, only keep sanitized keys
  const seen = new Set();
  const keys = [];
  dotenvText.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#')) return;
    const idx = line.indexOf('=');
    if (idx === -1) return;
    const key = line.slice(0, idx).trim();
    const sanitized = sanitizeKey(key);
    if (!sanitized) return;
    if (seen.has(sanitized)) return;
    seen.add(sanitized);
    keys.push(sanitized);
  });
  const lines = keys.map(k => `      ${k}: string;`);
  return `declare namespace NodeJS {
  interface ProcessEnv {
${lines.join('\n')}
  }
}
`;
}

module.exports = {
  generateEnvTypes,
};