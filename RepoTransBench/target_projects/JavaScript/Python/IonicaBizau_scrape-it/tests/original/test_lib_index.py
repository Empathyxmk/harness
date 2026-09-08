import pytest
from datetime import datetime

@pytest.fixture
def test_html():
    return """
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
    """

def test_scrape_html_selector_and_attr(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'title': 'h1.title',
        'descr': '.description',
        'date': {
            'selector': '.date',
            'convert': lambda d: datetime.strptime(d, '%Y-%m-%d')
        },
        'feats': {
            'listItem': '.features li',
            'how': 'html',
            'convert': lambda x: int(x)
        },
        'nested': {
            'selector': '.nested',
            'data': {
                'lev1': {
                    'selector': '.level1',
                    'data': {
                        'lev2': {
                            'selector': 'span',
                            'eq': 1
                        }
                    }
                }
            }
        }
    })
    assert result['data']['title'] == "Main Title"
    assert result['data']['descr'] == "A useful description here"
    assert result['data']['date'].timestamp() == datetime(2001, 11, 23).timestamp()
    assert isinstance(result['data']['feats'], list)
    assert result['data']['feats'][1] == 25
    assert result['data']['nested']['lev1']['lev2'] == "two"

def test_selector_not_found(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'notpresent': '.doesnotexist',
        'list': {'listItem': '.not-in-doc'}
    })
    assert result['data']['notpresent'] is None
    assert result['data']['list'] == []

def test_invalid_markup(scrapeIt):
    out = scrapeIt.scrapeHTML('garbage', {'some': 'h1'})
    assert out['data']['some'] == ""

def test_how_html_text_attr_eq(scrapeIt, test_html):
    result = scrapeIt.scrapeHTML(test_html, {
        'html': {
            'selector': 'div.description',
            'how': 'html'
        },
        'attr': {
            'selector': '.title',
            'attr': 'class'
        },
        'items': {
            'listItem': 'ul.features li',
            'eq': 0
        }
    })
    assert 'A useful' in result['data']['html']
    assert result['data']['attr'] == 'title'
    assert result['data']['items'] == "10"

def test_callback_api_success(scrapeIt, test_html):
    called = dict(err=None, data=None)
    def callback(err, data):
        called['err'] = err
        called['data'] = data
    scrapeIt.scrapeHTML(test_html, {'title': 'h1'}, callback)
    assert called['err'] is None
    assert called['data']['data']['title'] == 'Main Title'

def test_callback_api_with_error(scrapeIt):
    called = dict(err=None, data=None)
    def callback(err, data):
        called['err'] = err
        called['data'] = data
    scrapeIt('bad-url', None, callback)
    assert called['err'] is not None