const postcss = require('postcss');
const plugin = require('../index.js');

function processCSS(css) {
	return postcss([plugin()]).process(css, { from: undefined });
}

describe('postcss-write-svg (public)', () => {
	it('escapeWrappedQuotes escapes content values (public)', async () => {
		const css = `
			.eqpublic { background: url("data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg'>'foo\\'bar'</svg>"); }
		`;
		const result = await processCSS(css);
		const svg = decodeURIComponent(result.css);
		expect(svg.replace(/\\/g, '')).toContain("'foo'bar'");
	});

	it('escapeDoubleQuotes works in attributes (public)', async () => {
		const css = `
			.attrpublic { background: url("data:image/svg+xml;charset=utf-8,<svg xmlns=\\"http://www.w3.org/2000/svg\\">"foo\\"bar"</svg>"); }
		`;
		const result = await processCSS(css);
		const svg = decodeURIComponent(result.css);
		expect(svg.replace(/\\/g, '')).toContain('"foo"bar"');
	});
});