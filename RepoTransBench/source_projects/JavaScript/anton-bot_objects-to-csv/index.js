/**
 * Converts an array of objects to a CSV string.
 * @param {Object[]} arr - Array of objects to convert.
 * @param {Object} [options] - Options object.
 * @param {boolean} [options.header=true] - Whether to include header row.
 * @param {string[]} [options.fields] - Which fields to include (default: all keys found across all objects).
 * @param {string} [options.delimiter=","] - The CSV delimiter to use.
 * @returns {string} CSV string.
 */
function objectsToCsv(arr, options = {}) {
  if (!Array.isArray(arr)) {
    throw new TypeError("First argument must be an array.");
  }
  if (arr.length === 0) return "";
  const opts = Object.assign({ header: true, delimiter: "," }, options);
  let fields = opts.fields;
  if (!fields) {
    // Collect all unique keys from all objects
    fields = Array.from(
      arr.reduce((set, obj) => {
        Object.keys(obj).forEach(key => set.add(key));
        return set;
      }, new Set())
    );
  }
  // Build CSV
  const lines = [];
  if (opts.header) {
    lines.push(fields.map(f => `"${f.replace(/"/g, '""')}"`).join(opts.delimiter));
  }
  for (const obj of arr) {
    lines.push(fields
      .map(f => {
        let val = obj[f];
        // Null/undefined is empty
        if (val === undefined || val === null) return "";
        // Escape quotes by doubling them
        val = String(val).replace(/"/g, '""');
        // Enclose in quotes if contains delimiter, quote, or newline
        if (
          val.includes(opts.delimiter) ||
          val.includes('"') ||
          val.includes("\n") ||
          val.includes("\r")
        ) {
          val = `"${val}"`;
        }
        return val;
      })
      .join(opts.delimiter));
  }
  return lines.join("\n");
}

module.exports = objectsToCsv;