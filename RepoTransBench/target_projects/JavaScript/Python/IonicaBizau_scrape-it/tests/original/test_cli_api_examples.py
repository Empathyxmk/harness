import pytest
from datetime import datetime
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

@pytest.fixture(scope="module")
def http_server():
    html = """
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
    """

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        def log_message(self, format, *args):
            # Suppress logging
            pass

    server = HTTPServer(('localhost', 9001), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield 'http://localhost:9001'
    server.shutdown()
    server.server_close()
    thread.join()

def test_promise_interface_scrape(scrapeIt, http_server):
    out = scrapeIt(http_server, {
        "title": ".header h1",
        "desc": ".header h2",
        "avatar": {
            "selector": ".header img",
            "attr": "src"
        }
    })
    data, status = out['data'], out.get('status')
    assert status in (200, None)
    assert data['title'] == "MyTitle"
    assert "description" in data['desc']
    assert data['avatar'] == "/img/test.png"

def test_async_listitem_nested_conversions(scrapeIt, http_server):
    out = scrapeIt(http_server, {
        "articles": {
            "listItem": ".article",
            "data": {
                "createdAt": {
                    "selector": ".date",
                    "convert": lambda x: datetime.strptime(x, "%Y-%m-%d")
                },
                "title": "a.article-title",
                "tags": {
                    "listItem": ".tags > span"
                },
                "content": {
                    "selector": ".article-content",
                    "how": "html"
                }
            }
        },
        "pages": {
            "listItem": "li.page",
            "data": {
                "title": "a",
                "url": {
                    "selector": "a",
                    "attr": "href"
                }
            }
        },
        "title": ".header h1",
        "desc": ".header h2",
        "avatar": {
            "selector": ".header img",
            "attr": "src"
        }
    })
    data = out['data']
    assert len(data['articles']) > 0
    assert data['articles'][0]['title'] == "Async Article"
    assert data['articles'][0]['tags'] == ["tag1"]
    assert data['articles'][0]['createdAt'].year == 2020
    assert data['pages'][0]['title'] == "Page1"
    assert data['title'] == "MyTitle"
    assert ".png" in data['avatar']