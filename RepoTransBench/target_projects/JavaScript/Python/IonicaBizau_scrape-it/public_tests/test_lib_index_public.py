import pytest
from datetime import datetime

@pytest.fixture
def test_html():
    return """
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
    """

def test_scrape_html_public(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'headline': 'h1.main-title',
        'info': '.info',
        'timestamp': {
            'selector': '.timestamp',
            'convert': lambda d: datetime.strptime(d, '%Y-%m-%d')
        },
        'numbers': {
            'listItem': '.items li',
            'how': 'html',
            'convert': lambda x: int(x)
        },
        'structure': {
            'selector': '.container',
            'data': {
                'depth': {
                    'selector': '.depth1',
                    'data': {
                        'val': {
                            'selector': 'span',
                            'eq': 0
                        }
                    }
                }
            }
        }
    })
    assert result['data']['headline'] == "Alternate Title"
    assert result['data']['info'] == "A different paragraph here"
    assert result['data']['timestamp'].timestamp() == datetime(2011, 5, 3).timestamp()
    assert isinstance(result['data']['numbers'], list)
    assert result['data']['numbers'][1] == 99
    assert result['data']['structure']['depth']['val'] == "alpha"

def test_selector_not_found_public(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'missing': '.nonexistent-class',
        'anotherList': {'listItem': '.not-in-this-html'}
    })
    assert result['data']['missing'] is None
    assert result['data']['anotherList'] == []

def test_invalid_markup_edge_public(scrapeIt):
    out = scrapeIt.scrapeHTML('$$invalid%%markup', {'node': '.main-title'})
    assert out['data']['node'] == ""

def test_how_html_text_attr_eq_public(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'html': {
            'selector': 'div.info',
            'how': 'html'
        },
        'attr': {
            'selector': '.main-title',
            'attr': 'class'
        },
        'firstItem': {
            'listItem': 'ul.items li',
            'eq': 1
        }
    })
    assert 'different paragraph' in result['data']['html']
    assert result['data']['attr'] == 'main-title'
    assert result['data']['firstItem'] == "99"

def test_callback_api_success_public(scrapeIt, test_html):
    called = dict(err=None, data=None)
    def callback(err, data):
        called['err'] = err
        called['data'] = data
    scrapeIt.scrapeHTML(test_html, {'headline': 'h1'}, callback)
    assert called['err'] is None
    assert called['data']['data']['headline'] == 'Alternate Title'

def test_callback_api_with_error_public(scrapeIt):
    called = dict(err=None, data=None)
    def callback(err, data):
        called['err'] = err
        called['data'] = data
    scrapeIt('invalid-test-url', None, callback)
    assert called['err'] is not None