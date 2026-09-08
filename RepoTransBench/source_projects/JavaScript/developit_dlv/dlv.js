/**
 * dlv: Safe deep property access for JavaScript
 * @param {Object} obj - The object to query.
 * @param {string|array} key - The path of the property to get.
 * @param {*} [def] - The default value.
 * @returns {*} The resolved value.
 * 
 * Examples:
 * dlv({a:{b:2}}, 'a.b') // 2
 * dlv({a:{b:2}}, ['a','b']) // 2
 * dlv({a:{b:2}}, 'a.c', 'fallback') // 'fallback'
 */
function dlv(obj, key, def) {
	if (!obj) return def;
	if (typeof key === 'string') {
		key = key.split ? key.split('.') : [key];
	}
	for (var i = 0; i < key.length; i++) {
		if (typeof obj !== 'object' || obj === null || !(key[i] in obj)) {
			return def;
		}
		obj = obj[key[i]];
	}
	return obj === undefined ? def : obj;
}

module.exports = dlv;