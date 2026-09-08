from django import test
from django.conf import settings
from django_google_maps.widgets import GoogleMapsAddressWidget


class WidgetPublicTests(test.TestCase):
    def test_render_returns_custom_html(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('adam', 'customvalue', attrs={'id': 'unique', 'class': 'css-test'})
        expected = '<input id="unique" class="css-test" name="adam" type="text" value="customvalue" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_render_returns_blank_for_value_when_none_public(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('foo', None, attrs={'style': 'color:red;', 'data-bar': 'hello'})
        expected = '<input style="color:red;" data-bar="hello" name="foo" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_maps_js_api_key_different(self):
        widget = GoogleMapsAddressWidget()
        google_maps_js = "https://maps.google.com/maps/api/js?key={}&libraries=places".format(
            settings.GOOGLE_MAPS_API_KEY)
        self.assertEqual(google_maps_js, widget.Media().js[1])