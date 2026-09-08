// Public Jest tests covering the CLI/public API usage style, loading lib/index.js as module
// DATA AND SELECTORS ARE DIFFERENT FROM THE ORIGINAL

const scrapeIt = require('../../lib');
const http = require('http');

// Different HTML, structure is similar but all content and selectors differ!
const html = `
  <html>
    <header><title>Another Test</title></header>
    <body>
      <div class="banner">
        <h1>SitePublic</h1>
        <h2>Alternative public info</h2>
        <img src="/img/public.png"/>
      </div>
      <ul class="numbers">
        <li>5</li><li>8</li>
      </ul>
      <article class="content-section">
        <span class="pub-date">2019-12-12</span>
        <a class="headline-link">Public Article</a>
        <div class="labels"><span>publictag</span></div>
        <div class="main-content">Hi <i>everyone</i></div>
      </article>
      <li class="nav"><a href="/home">Home</a></li>
    </body>
  </html>
`;

let server;
let url;
beforeAll(done => {
  server = http.createServer((req, res) => {
    res.writeHead(200, {"Content-Type": "text/html"});
    res.end(html);
  }).listen(9011, () => {
    url = "http://localhost:9011";
    done();
  });
});

afterAll(done => {
  server.close(done);
});

// Promise interface test (public)
test("Promise interface should scrape title, desc, avatar [public]", async () => {
  const { data, status } = await scrapeIt(url, {
    title: ".banner h1",
    info: ".banner h2",
    image: {
      selector: ".banner img",
      attr: "src"
    }
  });
  expect([200, undefined]).toContain(status);
  expect(data.title).toBe("SitePublic")
  expect(data.info).toContain("Alternative")
  expect(data.image).toBe("/img/public.png")
});

// Async/await + listItem, nested, attribute and conversions (public)
test("Async/await interface handles listItem, nested and conversions [public]", async () => {
  const { data } = await scrapeIt(url, {
    articles: {
      listItem: ".content-section",
      data: {
        published: {
          selector: ".pub-date",
          convert: x => new Date(x)
        },
        headline: "a.headline-link",
        labels: {
          listItem: ".labels > span"
        },
        content: {
          selector: ".main-content",
          how: "html"
        }
      }
    },
    nav: {
      listItem: "li.nav",
      data: {
        title: "a",
        url: {
          selector: "a",
          attr: "href"
        }
      }
    },
    title: ".banner h1",
    info: ".banner h2",
    image: {
      selector: ".banner img",
      attr: "src"
    }
  });

  expect(data.articles.length).toBeGreaterThan(0)
  expect(data.articles[0].headline).toBe("Public Article")
  expect(data.articles[0].labels).toEqual(["publictag"])
  expect(data.articles[0].published.getFullYear()).toBe(2019)
  expect(data.nav[0].title).toBe("Home")
  expect(data.title).toBe("SitePublic")
  expect(data.image).toMatch(/\.png/)
});