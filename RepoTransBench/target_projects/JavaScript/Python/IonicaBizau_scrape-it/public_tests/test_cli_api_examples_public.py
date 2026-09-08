import pytest
from datetime import datetime
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

@pytest.fixture(scope="module")
def http_server():
    html = """
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

    server = HTTPServer(('localhost', 9011), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield 'http://localhost:9011'
    server.shutdown()
    server.server_close()
    thread.join()

def test_promise_interface_public(scrapeIt, http_server):
    out = scrapeIt(http_server, {
        "title": ".banner h1",
        "info": ".banner h2",
        "image": {
            "selector": ".banner img",
            "attr": "src"
        }
    })
    data, status = out['data'], out.get('status')
    assert status in (200, None)
    assert data['title'] == "SitePublic"
    assert "Alternative" in data['info']
    assert data['image'] == "/img/public.png"

def test_async_listitem_nested_conversions_public(scrapeIt, http_server):
    out = scrapeIt(http_server, {
        "articles": {
            "listItem": ".content-section",
            "data": {
                "published": {
                    "selector": ".pub-date",
                    "convert": lambda x: datetime.strptime(x, "%Y-%m-%d")
                },
                "headline": "a.headline-link",
                "labels": {
                    "listItem": ".labels > span"
                },
                "content": {
                    "selector": ".main-content",
                    "how": "html"
                }
            }
        },
        "nav": {
            "listItem": "li.nav",
            "data": {
                "title": "a",
                "url": {
                    "selector": "a",
                    "attr": "href"
                }
            }
        },
        "title": ".banner h1",
        "info": ".banner h2",
        "image": {
            "selector": ".banner img",
            "attr": "src"
        }
    })
    data = out['data']
    assert len(data['articles']) > 0
    assert data['articles'][0]['headline'] == "Public Article"
    assert data['articles'][0]['labels'] == ["publictag"]
    assert data['articles'][0]['published'].year == 2019
    assert data['nav'][0]['title'] == "Home"
    assert data['title'] == "SitePublic"
    assert ".png" in data['image']