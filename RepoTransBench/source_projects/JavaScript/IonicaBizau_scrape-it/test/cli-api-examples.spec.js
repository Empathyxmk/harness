// Jest tests covering the CLI/public API usage style, loading lib/index.js as module
// Covers main README example usage for scrapeIt(url, ...) and async usage

const scrapeIt = require('../lib');
const http = require('http');

const html = `
  <html>
    <header><title>My Test</title></header>
    <body>
      <div class="header">
        <h1>MyTitle</h1>
        <h2>Some description here</h2>
        <img src="/img/test.png"/>
      </div>
      <ul class="features">
        <li>1</li><li>2</li>
      </ul>
      <div class="article">
        <span class="date">2020-01-01</span>
        <a class="article-title">Async Article</a>
        <div class="tags"><span>tag1</span></div>
        <div class="article-content">Hello <b>world</b></div>
      </div>
      <li class="page"><a href="/page1">Page1</a></li>
    </body>
  </html>
`;

let server;
let url;
beforeAll(done => {
  server = http.createServer((req, res) => {
    res.writeHead(200, {"Content-Type": "text/html"});
    res.end(html);
  }).listen(9001, () => {
    url = "http://localhost:9001";
    done();
  });
});

afterAll(done => {
  server.close(done);
});

// Promise interface test
test("Promise interface should scrape title, desc, avatar", async () => {
  const { data, status } = await scrapeIt(url, {
    title: ".header h1",
    desc: ".header h2",
    avatar: {
      selector: ".header img",
      attr: "src"
    }
  });
  expect([200, undefined]).toContain(status); // returns 200 if using request, else undefined with scrapeHTML
  expect(data.title).toBe("MyTitle")
  expect(data.desc).toContain("description")
  expect(data.avatar).toBe("/img/test.png")
});

// Async/await + listItem, nested, attribute and conversions
test("Async/await interface handles listItem, nested and conversions", async () => {
  const { data } = await scrapeIt(url, {
    articles: {
      listItem: ".article",
      data: {
        createdAt: {
          selector: ".date",
          convert: x => new Date(x)
        },
        title: "a.article-title",
        tags: {
          listItem: ".tags > span"
        },
        content: {
          selector: ".article-content",
          how: "html"
        }
      }
    },
    pages: {
      listItem: "li.page",
      data: {
        title: "a",
        url: {
          selector: "a",
          attr: "href"
        }
      }
    },
    title: ".header h1",
    desc: ".header h2",
    avatar: {
      selector: ".header img",
      attr: "src"
    }
  });

  expect(data.articles.length).toBeGreaterThan(0)
  expect(data.articles[0].title).toBe("Async Article")
  expect(data.articles[0].tags).toEqual(["tag1"])
  expect(data.articles[0].createdAt.getFullYear()).toBe(2020)
  expect(data.pages[0].title).toBe("Page1")
  expect(data.title).toBe("MyTitle")
  expect(data.avatar).toMatch(/\.png/)
});