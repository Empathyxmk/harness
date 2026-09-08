use crate::data::JsonApiResponse;
use serde_json::json;

#[test]
fn test_keeps_example_public() {
    let another_example_response = json!({
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
    });
    let resp = JsonApiResponse::from_data(another_example_response.clone());
    assert_eq!(resp.as_data(), another_example_response);
}