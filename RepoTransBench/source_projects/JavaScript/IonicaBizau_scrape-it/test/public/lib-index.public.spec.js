// Public Jest test for core lib/index.js (scrape-it) covering API surface, errors and major options
// DATA AND SELECTORS ARE DIFFERENT FROM ORIGINAL SPEC FILE!

const path = require('path');
const fs = require('fs');
const scrapeIt = require('../../lib');
const testHtml = `
<html>
  <head><title>My Public Test</title></head>
  <body>
    <h1 class="main-title">Alternate Title</h1>
    <div class="info">A different paragraph here</div>
    <span class="timestamp">2011-05-03</span>
    <ul class="items">
      <li>42</li>
      <li>99</li>
    </ul>
    <section class="container">
      <div class="bar">
        <div class="depth1">
          <span>alpha</span>
          <span>beta</span>
        </div>
        <span class="depth2">Ultimate</span>
      </div>
    </section>
    <div class="not-used"></div>
  </body>
</html>
`;

describe("scrape-it public tests (lib/index.js)", () => {
  it("should scrape HTML string (scrapeHTML) with selector & attr features (public)", async () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      headline: "h1.main-title",
      info: ".info",
      timestamp: {
        selector: ".timestamp",
        convert: (d) => new Date(d)
      },
      numbers: {
        listItem: ".items li",
        how: 'html',
        convert: (x) => parseInt(x, 10)
      },
      structure: {
        selector: ".container",
        data: {
          depth: {
            selector: ".depth1",
            data: {
              val: {
                selector: "span",
                eq: 0
              }
            }
          }
        }
      }
    });
    // Data shape assertions, all values different from original
    expect(result.data.headline).toBe("Alternate Title")
    expect(result.data.info).toBe("A different paragraph here")
    expect(result.data.timestamp.getTime()).toBe(new Date("2011-05-03").getTime())
    expect(Array.isArray(result.data.numbers)).toBeTruthy()
    expect(result.data.numbers[1]).toBe(99)
    expect(result.data.structure.depth.val).toBe("alpha")
  });

  it("should handle when selector not found (returns undefined/null or empty list) [public]", () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      missing: ".nonexistent-class",
      anotherList: { listItem: ".not-in-this-html" }
    });
    expect(result.data.missing).toBe(undefined)
    expect(result.data.anotherList).toEqual([])
  });

  it('should handle invalid markup edge (public)', () => {
    // Differs from existing: using another garbage string
    const out = scrapeIt.scrapeHTML('$$invalid%%markup', { node: ".main-title" });
    expect(out.data.node).toEqual(""); // No match
  });

  it('should support how/html/text, attr and eq for lists (public)', () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      html: {
        selector: "div.info",
        how: "html"
      },
      attr: {
        selector: ".main-title",
        attr: "class"
      },
      firstItem: {
        listItem: "ul.items li",
        eq: 1
      }
    });
    expect(result.data.html).toContain('different paragraph')
    expect(result.data.attr).toBe('main-title')
    expect(result.data.firstItem).toBe("99")
  });

  it('should handle callback API with success (public)', done => {
    scrapeIt.scrapeHTML(testHtml, { headline: "h1" }, (err, data) => {
      expect(err).toBeNull();
      expect(data.data.headline).toBe('Alternate Title');
      done();
    });
  });

  it('should handle callback API with error (invalid options, public)', done => {
    // Just as in regular test, but still different; string changes
    scrapeIt('invalid-test-url', null, (err, data) => {
      expect(err).not.toBeNull();
      done();
    });
  });
});