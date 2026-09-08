import jsonapi_requests.data


class TestJsonApiResponsePublic:
    def test_keeps_example_public(self):
        assert jsonapi_requests.data.JsonApiResponse.from_data(another_example_response).as_data() == another_example_response

    def test_links_always_present_in_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({})
        parsed.links['yyy'] = 'faked'
        assert parsed.as_data() == {'links': {'yyy': 'faked'}}

    def test_add_object_to_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({'data': []})
        parsed.data.append({'id': '3', 'type': 'y'})
        assert parsed.as_data() == {'data': [{'id': '3', 'type': 'y'}]}

    def test_remove_object_from_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({'data': [{'id': '3', 'type': 'y'}]})
        del parsed.data[0]
        assert parsed.as_data() == {'data': []}

    def test_add_included_object_to_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({'included': [{'id': '3', 'type': 'y'}]})
        del parsed.included[0]
        assert parsed.as_data() == {}

    def test_remove_included_object_from_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({})
        parsed.included.append({'id': '3', 'type': 'y'})
        assert parsed.as_data() == {'included': [{'id': '3', 'type': 'y'}]}

    def test_add_relationship_to_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data({})
        parsed.data.relationships['duck'] = {'data': {'type': 'duck', 'id': '9'}}
        assert parsed.as_data() == {'data': {'relationships': {'duck': {'data': {'type': 'duck', 'id': '9'}}}}}

    def test_remove_relationship_from_parsed_response_public(self):
        parsed = jsonapi_requests.data.JsonApiResponse.from_data(
          {'data': {'relationships': {'duck': {'data': {'type': 'duck', 'id': '9'}}}}},
        )
        del parsed.data.relationships['duck']
        assert parsed.as_data() == {}


another_example_response = {
  "links": {
    "self": "http://other.com/books",
    "next": "http://other.com/books?page[offset]=5",
    "last": "http://other.com/books?page[offset]=20",
  },
  "data": [{
    "type": "books",
    "id": "3",
    "attributes": {
      "title": "JSON API for humans!",
    },
    "relationships": {
      "editor": {
        "links": {
          "self": "http://other.com/books/3/relationships/editor",
          "related": "http://other.com/books/3/editor",
        },
        "data": {"type": "people", "id": "21"},
      },
      "chapters": {
        "links": {
          "self": "http://other.com/books/3/relationships/chapters",
          "related": "http://other.com/books/3/chapters",
        },
        "data": [
          {"type": "chapters", "id": "4"},
          {"type": "chapters", "id": "8"},
        ],
      },
    },
    "links": {
      "self": "http://other.com/books/3",
    },
  }],
  "included": [{
    "type": "people",
    "id": "21",
    "attributes": {
      "first-name": "Ana",
      "last-name": "Smith",
      "twitter": "anasmith",
    },
    "links": {
      "self": "http://other.com/people/21",
    },
  }, {
    "type": "chapters",
    "id": "4",
    "attributes": {
      "title": "Prologue",
    },
    "links": {
      "self": "http://other.com/chapters/4",
    },
  }, {
    "type": "chapters",
    "id": "8",
    "attributes": {
      "title": "Epilogue",
    },
    "links": {
      "self": "http://other.com/chapters/8",
    },
  }],
}