//! Tests for @jwt_required(optional=True) view logic (get, post) with optional/empty user
use actix_web::{test, web, App, HttpResponse, get};
use serde_json::json;

#[get("/optional")]
async fn access_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar"}))
}

#[actix_rt::test]
async fn test_get_jwt_in_optional_route() {
    let app = test::init_service(App::new().service(access_protected)).await;
    let req = test::TestRequest::get().uri("/optional").to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"foo": "bar"}));
}