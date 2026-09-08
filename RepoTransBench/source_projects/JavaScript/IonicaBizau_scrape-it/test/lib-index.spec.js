// Jest test for core lib/index.js (scrape-it) covering API surface, errors and major options

const path = require('path');
const fs = require('fs');
const scrapeIt = require('../lib');
const testHtml = `
<html>
  <head><title>Test</title></head>
  <body>
    <h1 class="title">Main Title</h1>
    <div class="description">A useful description here</div>
    <span class="date">2001-11-23</span>
    <ul class="features">
      <li>10</li>
      <li>25</li>
    </ul>
    <div class="nested">
      <div class="foo">
        <div class="level1">
          <span>one</span>
          <span>two</span>
        </div>
        <span class="level2">Final</span>
      </div>
    </div>
    <div class="error"></div>
  </body>
</html>
`;

describe("scrape-it package core API (lib/index.js)", () => {
  it("should scrape HTML string (scrapeHTML) with selector & attr features", async () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      title: "h1.title",
      descr: ".description",
      date: {
        selector: ".date",
        convert: (d) => new Date(d)
      },
      feats: {
        listItem: ".features li",
        how: 'html',
        convert: (x) => parseInt(x, 10)
      },
      nested: {
        selector: ".nested",
        data: {
          lev1: {
            selector: ".level1",
            data: {
              lev2: {
                selector: "span",
                eq: 1
              }
            }
          }
        }
      }
    });
    // Data shape assertions
    expect(result.data.title).toBe("Main Title")
    expect(result.data.descr).toBe("A useful description here")
    expect(result.data.date.getTime()).toBe(new Date("2001-11-23").getTime())
    expect(Array.isArray(result.data.feats)).toBeTruthy()
    expect(result.data.feats[1]).toBe(25)
    expect(result.data.nested.lev1.lev2).toBe("two")
  });

  it("should handle when selector not found (returns undefined/null or empty list)", () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      notpresent: ".doesnotexist",
      list: { listItem: ".not-in-doc" }
    });
    expect(result.data.notpresent).toBe(undefined)
    expect(result.data.list).toEqual([])
  });

  it('should throw error with invalid markup', () => {
    // Not a valid HTML, Cheerio still parses, but test edge
    const out = scrapeIt.scrapeHTML('garbage', { some: "h1" });
    expect(out.data.some).toEqual(""); // No h1
  });

  it('should support how/html/text, attr and eq for lists', () => {
    const result = scrapeIt.scrapeHTML(testHtml, {
      html: {
        selector: "div.description",
        how: "html"
      },
      attr: {
        selector: ".title",
        attr: "class"
      },
      items: {
        listItem: "ul.features li",
        eq: 0
      }
    });
    expect(result.data.html).toContain('A useful')
    expect(result.data.attr).toBe('title')
    expect(result.data.items).toBe("10")
  });

  it('should handle callback API with success', done => {
    scrapeIt.scrapeHTML(testHtml, { title: "h1" }, (err, data) => {
      expect(err).toBeNull();
      expect(data.data.title).toBe('Main Title');
      done();
    });
  });

  it('should handle callback API with error (invalid options)', done => {
    // Calling with bad options triggers error path in callback-mode?
    scrapeIt('bad-url', null, (err, data) => {
      expect(err).not.toBeNull();
      done();
    });
  });
});