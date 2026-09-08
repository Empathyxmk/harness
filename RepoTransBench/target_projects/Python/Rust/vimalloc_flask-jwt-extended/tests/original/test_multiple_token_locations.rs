//! Test JWT in multiple locations (partial)
use actix_web::{test, web, App, HttpResponse, get, post};
use serde_json::json;

#[get("/cookie_login")]
async fn cookie_login() -> HttpResponse {
    HttpResponse::Ok().json(json!({"login": true}))
}
#[get("/protected")]
async fn access_protected() -> HttpResponse {
    HttpResponse::Ok().json(json!({"foo": "bar", "location": "headers"}))
}
#[actix_rt::test]
async fn test_header_access() {
    let app = test::init_service(App::new().service(cookie_login).service(access_protected)).await;
    let req = test::TestRequest::get().uri("/protected").to_request();
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), 200);
    let val: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(val, json!({"foo": "bar", "location": "headers"}));
}